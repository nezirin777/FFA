// FFA共通UI: 通知、二重送信防止、画面遷移、表示設定をまとめて管理する。
(() => {
  "use strict";

  // 通知キューと画面ロックの状態。ページ内で一度に一つだけ通知を表示する。
  const toastQueue = [];
  const disabledState = new WeakMap();
  let showingToast = false;
  let uiLocked = false;
  let uiLockTimeout = null;
  let confirmOpen = false;

  // localStorageへ保存するUI設定と、許可する値の一覧。
  const DEFAULT_TIMEOUT_SECONDS = 25;
  const TOAST_POSITION_KEY = "toast-position";
  const DEFAULT_TOAST_POSITION = "toast-top-center";
  const NUMBER_FORMAT_KEY = "number-format";
  const DEFAULT_NUMBER_FORMAT = "plain";
  const TOAST_POSITIONS = [
    "toast-top-center",
    "toast-center",
    "toast-bottom-center",
    "toast-bottom-left",
    "toast-bottom-right",
  ];
  const NUMBER_FORMATS = ["comma", "plain"];
  const originalNumberText = new WeakMap();

  // 各画面に対象要素がある機能だけを初期化するため、ページ固有のJSは不要。
  document.addEventListener("DOMContentLoaded", () => {
    loadToastPosition();
    initToastPositionSelector();
    loadNumberFormat();
    initNumberFormatSelector();
    initCountdowns();
    initFacilityDescriptions();
    initSelectableRows();
    initHistoryButtons();

    const flashes = Array.isArray(window.FFA_FLASH_MESSAGES)
      ? window.FFA_FLASH_MESSAGES
      : [];

    flashes.forEach((flash) => {
      if (!flash || !flash.message) return;
      showToast(
        flash.message,
        flash.type || "info",
        Number.parseInt(flash.duration, 10) || 3500
      );
    });
  });

  // --- トースト表示位置 -------------------------------------------------

  // 保存値やdata属性の想定外値を既定値へ戻す。
  function normalizeToastPosition(position) {
    return TOAST_POSITIONS.includes(position)
      ? position
      : DEFAULT_TOAST_POSITION;
  }

  // コンテナの位置クラス、設定ボタン、保存値をまとめて更新する。
  function setToastPosition(position, persist = true) {
    const nextPosition = normalizeToastPosition(position);
    const container = document.getElementById("toast-container");

    if (container) {
      container.classList.remove(...TOAST_POSITIONS);
      container.classList.add(nextPosition);
    }

    document.querySelectorAll(".toast-position-btn").forEach((button) => {
      const active = button.dataset.position === nextPosition;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });

    if (persist) {
      try {
        localStorage.setItem(TOAST_POSITION_KEY, nextPosition);
      } catch {
        // localStorage が使えない環境では現在ページ内の反映だけ行う。
      }
    }

    return nextPosition;
  }

  // 保存済みの位置を読み込み、保存処理を行わずに画面へ反映する。
  function loadToastPosition() {
    let savedPosition = DEFAULT_TOAST_POSITION;
    try {
      savedPosition = localStorage.getItem(TOAST_POSITION_KEY) || DEFAULT_TOAST_POSITION;
    } catch {
      savedPosition = DEFAULT_TOAST_POSITION;
    }
    setToastPosition(savedPosition, false);
  }

  // 位置選択ボタンはイベント委譲で扱い、ボタン数の増減に追従する。
  function initToastPositionSelector() {
    document.querySelectorAll(".toast-position-selector").forEach((selector) => {
      selector.addEventListener("click", (event) => {
        const target = event.target;
        if (!target || typeof target.closest !== "function") return;

        const button = target.closest(".toast-position-btn");
        if (!button || !selector.contains(button)) return;

        const nextPosition = setToastPosition(button.dataset.position);
        const label = button.textContent.trim() || nextPosition;
        showToast(`メッセージ表示位置を「${label}」に変更しました。`, "success", 2000);
      });
    });
  }

  // --- 数値表示形式 -----------------------------------------------------

  // 表示形式も許可リスト以外は既定の「区切りなし」に戻す。
  function normalizeNumberFormat(format) {
    return NUMBER_FORMATS.includes(format) ? format : DEFAULT_NUMBER_FORMAT;
  }

  // ボタンの選択状態と本文中の数値を同期し、必要なら設定を保存する。
  function setNumberFormat(format, persist = true) {
    const nextFormat = normalizeNumberFormat(format);

    document.querySelectorAll(".number-format-btn").forEach((button) => {
      const active = button.dataset.numberFormat === nextFormat;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });

    if (persist) {
      try {
        localStorage.setItem(NUMBER_FORMAT_KEY, nextFormat);
      } catch {
        // localStorageが使えない環境では現在ページ内の反映だけ行う。
      }
    }

    applyNumberFormat(nextFormat);
    return nextFormat;
  }

  // 画面を移動しても同じ数値表示形式を使えるよう保存値を復元する。
  function loadNumberFormat() {
    let savedFormat = DEFAULT_NUMBER_FORMAT;
    try {
      savedFormat = localStorage.getItem(NUMBER_FORMAT_KEY) || DEFAULT_NUMBER_FORMAT;
    } catch {
      savedFormat = DEFAULT_NUMBER_FORMAT;
    }
    setNumberFormat(savedFormat, false);
  }

  // 数値表示の切替操作。トーストで変更結果も知らせる。
  function initNumberFormatSelector() {
    document.querySelectorAll(".number-format-selector").forEach((selector) => {
      selector.addEventListener("click", (event) => {
        const target = event.target;
        if (!target || typeof target.closest !== "function") return;

        const button = target.closest(".number-format-btn");
        if (!button || !selector.contains(button)) return;

        const nextFormat = setNumberFormat(button.dataset.numberFormat);
        const label = button.textContent.trim() || nextFormat;
        showToast(`数値表示を「${label}」に変更しました。`, "success", 2000);
      });
    });
  }

  // テキストノードだけを走査し、入力欄・ボタン・スクリプトの値は変更しない。
  function applyNumberFormat(format) {
    if (!document.body) return;

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node = walker.nextNode();
    while (node) {
      const parent = node.parentElement;
      const skip = !parent || parent.closest(
        "script, style, textarea, input, select, option, button, [data-number-format='off']"
      );

      if (!skip) {
        // 元の文字列を一度だけ保存し、区切りなしへ正確に戻せるようにする。
        if (!originalNumberText.has(node)) {
          originalNumberText.set(node, node.nodeValue || "");
        }
        const original = originalNumberText.get(node);
        node.nodeValue = format === "comma"
          ? addNumberCommas(original)
          : original;
      }

      node = walker.nextNode();
    }
  }

  function addNumberCommas(text) {
    // 4桁以上の数値だけを対象にし、FF10のような名前中の数字は変更しない。
    return text.replace(
      /(^|[^\w])([+-]?)([1-9]\d{3,})(?!\w)/g,
      (_match, prefix, sign, digits) => `${prefix}${sign}${digits.replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`
    );
  }

  // --- data属性で動く画面部品 ------------------------------------------

  // 待機時間を1秒ごとに更新し、終了時に指定された操作フォームを表示する。
  function initCountdowns() {
    document.querySelectorAll("[data-countdown-seconds]").forEach((element) => {
      let remaining = Number.parseInt(element.dataset.countdownSeconds, 10);
      if (!Number.isFinite(remaining) || remaining <= 0) return;

      const template = element.dataset.countdownTemplate || "あと {seconds} 秒";
      const render = () => {
        element.textContent = template.replace("{seconds}", String(remaining));
      };

      render();
      const timer = window.setInterval(() => {
        remaining -= 1;
        if (remaining > 0) {
          render();
          return;
        }

        window.clearInterval(timer);
        const targetId = element.dataset.countdownRevealTarget;
        const target = targetId ? document.getElementById(targetId) : null;
        if (target) {
          element.setAttribute("hidden", "");
          target.removeAttribute("hidden");
          return;
        }

        element.textContent = "利用できます";
      }, 1000);
    });
  }

  // 施設ボタンの説明は、マウスとキーボード操作の両方で同じ内容を表示する。
  function initFacilityDescriptions() {
    const description = document.querySelector("[data-facility-description-target]");
    if (!description) return;

    const defaultText = description.dataset.defaultDescription || description.textContent.trim();
    const setDescription = (text) => {
      description.textContent = text || defaultText;
    };

    document.querySelectorAll("[data-facility-description]").forEach((control) => {
      const text = control.dataset.facilityDescription;
      control.addEventListener("pointerenter", () => setDescription(text));
      control.addEventListener("focus", () => setDescription(text));
      control.addEventListener("pointerleave", () => setDescription(defaultText));
      control.addEventListener("blur", () => setDescription(defaultText));
    });
  }

  // 表の行を押してラジオボタンを選ぶ画面では、直接選択やキーボード操作にも表示を同期する。
  function initSelectableRows() {
    document.querySelectorAll("[data-selectable-row]").forEach((row) => {
      const radio = row.querySelector("input[type='radio']");
      const table = row.closest("table");
      if (!radio || !table) return;

      const updateSelection = () => {
        table.querySelectorAll("[data-selectable-row]").forEach((candidate) => {
          const candidateRadio = candidate.querySelector("input[type='radio']");
          candidate.classList.toggle("is-selected", Boolean(candidateRadio?.checked));
        });
      };

      row.addEventListener("click", (event) => {
        if (event.target.closest("input, label, button, a")) return;
        radio.checked = true;
        radio.dispatchEvent(new Event("change", { bubbles: true }));
      });
      radio.addEventListener("change", updateSelection);
      updateSelection();
    });
  }

  // data-history-back付きの戻るボタンに、HTMLから分離した履歴操作を付与する。
  function initHistoryButtons() {
    document.querySelectorAll("[data-history-back]").forEach((button) => {
      button.addEventListener("click", () => window.history.back());
    });
  }

  // --- フォーム送信・画面遷移の二重実行防止 ----------------------------

  // 送信中は全操作をロックする。data-confirm付きフォームは確認後に送信する。
  document.addEventListener("submit", async (event) => {
    if (event.defaultPrevented) return;

    const form = event.target;
    if (!form || form.tagName !== "FORM") return;
    if (form.dataset.noLock === "true") return;

    if (uiLocked) {
      event.preventDefault();
      showToast("処理中です。完了までお待ちください。", "info");
      return;
    }

    const confirmMessage = form.dataset.confirm;
    if (confirmMessage) {
      event.preventDefault();
      const ok = await showConfirm(confirmMessage);
      if (!ok) return;

      setUILock(true, getLoadingMessage(form), getTimeoutSeconds(form));
      try {
        HTMLFormElement.prototype.submit.call(form);
      } catch (err) {
        setUILock(false);
        throw err;
      }
      return;
    }

    setUILock(true, getLoadingMessage(form), getTimeoutSeconds(form));
  });

  // 同一タブ内リンクの遷移中にもロックを掛ける。新規タブやダウンロードは対象外。
  document.addEventListener("click", (event) => {
    if (event.defaultPrevented) return;
    if (event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    const link = event.target.closest ? event.target.closest("a[href]") : null;
    if (!link) return;
    if (link.dataset.noLock === "true") return;
    if (link.target && link.target !== "_self") return;
    if (link.hasAttribute("download")) return;

    const href = link.getAttribute("href") || "";
    if (!href || href.startsWith("#")) return;
    if (/^(javascript:|mailto:|tel:)/i.test(href)) return;

    let url;
    try {
      url = new URL(href, window.location.href);
    } catch {
      return;
    }

    if (
      url.origin === window.location.origin
      && url.pathname === window.location.pathname
      && url.search === window.location.search
      && url.hash
    ) {
      return;
    }

    if (uiLocked) {
      event.preventDefault();
      showToast("処理中です。完了までお待ちください。", "info");
      return;
    }

    setUILock(
      true,
      link.dataset.loading || "移動中...",
      getTimeoutSeconds(link)
    );
  });

  // data属性で画面ごとのロック文言・タイムアウトを必要な場合だけ上書きできる。
  function getLoadingMessage(element) {
    return element.dataset.loading || "処理中...";
  }

  function getTimeoutSeconds(element) {
    const raw = Number.parseInt(element.dataset.timeout, 10);
    return Number.isFinite(raw) && raw > 0 ? raw : DEFAULT_TIMEOUT_SECONDS;
  }

  // オーバーレイ表示、操作部品の無効化、タイムアウト解除を一箇所で管理する。
  function setUILock(locked, message = "処理中...", timeoutSeconds = DEFAULT_TIMEOUT_SECONDS) {
    const overlay = document.getElementById("overlay");
    const buttons = document.querySelectorAll(
      "button, input[type='button'], input[type='submit']"
    );

    if (uiLockTimeout) {
      clearTimeout(uiLockTimeout);
      uiLockTimeout = null;
    }

    uiLocked = Boolean(locked);

    if (overlay) {
      overlay.classList.toggle("hidden", !uiLocked);
      overlay.setAttribute("aria-hidden", uiLocked ? "false" : "true");

      const messageEl = overlay.querySelector(".overlay-text");
      if (messageEl) {
        messageEl.textContent = message || "処理中...";
      }
    }

    buttons.forEach((button) => {
      if (uiLocked) {
        if (!disabledState.has(button)) {
          disabledState.set(button, button.disabled);
        }
        button.disabled = true;
      } else if (disabledState.has(button)) {
        button.disabled = disabledState.get(button);
        disabledState.delete(button);
      }
    });

    document.body.classList.toggle("ui-locked", uiLocked);
    document.body.style.cursor = uiLocked ? "wait" : "";

    if (uiLocked) {
      uiLockTimeout = setTimeout(() => {
        setUILock(false);
        showToast("通信がタイムアウトしました。もう一度お試しください。", "error", 5000);
      }, timeoutSeconds * 1000);
    }
  }

  // 戻る操作・通信失敗・例外ではロックを残さず、再操作できる状態へ戻す。
  window.addEventListener("pageshow", () => {
    setUILock(false);
  });

  window.addEventListener("error", () => {
    setUILock(false);
  });

  window.addEventListener("unhandledrejection", () => {
    setUILock(false);
  });

  window.addEventListener("beforeunload", () => {
    if (uiLockTimeout) {
      clearTimeout(uiLockTimeout);
      uiLockTimeout = null;
    }

    window.addEventListener("focus", () => {
      setUILock(false);
    }, { once: true });
  });

  // 確認ダイアログを開いていないときだけ、Escで待機ロックを手動解除できる。
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || confirmOpen) return;
    if (!uiLocked) return;
    setUILock(false);
    showToast("処理ロックを解除しました。", "info");
  });

  // 共通モーダルを使う確認ダイアログ。テンプレートに無い画面では標準確認へフォールバックする。
  function showConfirm(message) {
    return new Promise((resolve) => {
      if (confirmOpen) {
        resolve(false);
        return;
      }

      const modal = document.getElementById("confirm-modal");
      const messageEl = document.getElementById("confirm-message");
      const okButton = document.getElementById("confirm-ok");
      const cancelButton = document.getElementById("confirm-cancel");

      if (!modal || !messageEl || !okButton || !cancelButton) {
        resolve(window.confirm(message));
        return;
      }

      confirmOpen = true;
      messageEl.textContent = message;
      modal.classList.remove("hidden");
      okButton.focus();

      const cleanup = (result) => {
        modal.classList.add("hidden");
        okButton.removeEventListener("click", onOk);
        cancelButton.removeEventListener("click", onCancel);
        modal.removeEventListener("click", onBackdrop);
        document.removeEventListener("keydown", onKeydown);
        confirmOpen = false;
        resolve(result);
      };

      const onOk = () => cleanup(true);
      const onCancel = () => cleanup(false);
      const onBackdrop = (event) => {
        if (event.target === modal) cleanup(false);
      };
      const onKeydown = (event) => {
        if (event.key === "Enter") cleanup(true);
        if (event.key === "Escape") cleanup(false);
      };

      okButton.addEventListener("click", onOk);
      cancelButton.addEventListener("click", onCancel);
      modal.addEventListener("click", onBackdrop);
      document.addEventListener("keydown", onKeydown);
    });
  }

  // --- トースト通知 -----------------------------------------------------

  // 通知をキューへ積み、表示中の通知が終わってから順に描画する。
  function showToast(message, type = "info", duration = 3500) {
    const cleanType = ["success", "error", "warning", "info"].includes(type)
      ? type
      : "info";
    toastQueue.push({
      message: String(message),
      type: cleanType,
      duration: Math.max(1000, Math.min(Number(duration) || 3500, 10000)),
    });
    processToastQueue();
  }

  // 一つの通知を表示・フェードアウトし、次の通知へ進む。
  async function processToastQueue() {
    if (showingToast || toastQueue.length === 0) return;

    const container = document.getElementById("toast-container");
    if (!container) return;

    showingToast = true;
    const toastData = toastQueue.shift();
    const toast = document.createElement("div");
    toast.className = `toast toast--${toastData.type}`;
    toast.setAttribute("role", "status");
    toast.textContent = toastData.message;
    container.appendChild(toast);
    applyNumberFormat(getStoredNumberFormat());

    await sleep(toastData.duration);
    toast.classList.add("toast--fade-out");
    await sleep(200);
    toast.remove();
    showingToast = false;
    processToastQueue();
  }

  function sleep(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  }

  // 動的に追加したトーストにも現在の数値表示形式を適用するための取得処理。
  function getStoredNumberFormat() {
    try {
      return normalizeNumberFormat(localStorage.getItem(NUMBER_FORMAT_KEY));
    } catch {
      return DEFAULT_NUMBER_FORMAT;
    }
  }

  // JavaScriptからPOST遷移が必要な場合だけ使う。CSRFトークンは呼び出し側で渡す。
  function postNavigate(url, params = {}) {
    setUILock(true, "移動中...");
    const form = document.createElement("form");
    form.method = "POST";
    form.action = url;

    Object.keys(params).forEach((key) => {
      const input = document.createElement("input");
      input.type = "hidden";
      input.name = key;
      input.value = params[key];
      form.appendChild(input);
    });

    document.body.appendChild(form);
    try {
      HTMLFormElement.prototype.submit.call(form);
    } catch (err) {
      setUILock(false);
      throw err;
    }
  }

  // fetch中も同じロックとエラー通知を使い、呼び出し側には失敗を再送出する。
  async function safeFetch(url, options = {}) {
    try {
      setUILock(true, "読み込み中...");
      const response = await fetch(url, options);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response;
    } catch (err) {
      setUILock(false);
      showToast("通信に失敗しました。", "error", 5000);
      throw err;
    } finally {
      setUILock(false);
    }
  }

  // テンプレート内の小さなスクリプトから利用する公開API。
  window.showToast = showToast;
  window.setUILock = setUILock;
  window.setToastPosition = setToastPosition;
  window.setNumberFormat = setNumberFormat;
  window.postNavigate = postNavigate;
  window.safeFetch = safeFetch;
})();
