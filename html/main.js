// FFA common UI helpers: toast, transition lock, safe navigation.
(() => {
  "use strict";

  const toastQueue = [];
  const disabledState = new WeakMap();
  let showingToast = false;
  let uiLocked = false;
  let uiLockTimeout = null;
  let confirmOpen = false;

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

  document.addEventListener("DOMContentLoaded", () => {
    loadToastPosition();
    initToastPositionSelector();
    loadNumberFormat();
    initNumberFormatSelector();
    initCountdowns();

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

  function normalizeToastPosition(position) {
    return TOAST_POSITIONS.includes(position)
      ? position
      : DEFAULT_TOAST_POSITION;
  }

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

  function loadToastPosition() {
    let savedPosition = DEFAULT_TOAST_POSITION;
    try {
      savedPosition = localStorage.getItem(TOAST_POSITION_KEY) || DEFAULT_TOAST_POSITION;
    } catch {
      savedPosition = DEFAULT_TOAST_POSITION;
    }
    setToastPosition(savedPosition, false);
  }

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

  function normalizeNumberFormat(format) {
    return NUMBER_FORMATS.includes(format) ? format : DEFAULT_NUMBER_FORMAT;
  }

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

  function loadNumberFormat() {
    let savedFormat = DEFAULT_NUMBER_FORMAT;
    try {
      savedFormat = localStorage.getItem(NUMBER_FORMAT_KEY) || DEFAULT_NUMBER_FORMAT;
    } catch {
      savedFormat = DEFAULT_NUMBER_FORMAT;
    }
    setNumberFormat(savedFormat, false);
  }

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

  function getLoadingMessage(element) {
    return element.dataset.loading || "処理中...";
  }

  function getTimeoutSeconds(element) {
    const raw = Number.parseInt(element.dataset.timeout, 10);
    return Number.isFinite(raw) && raw > 0 ? raw : DEFAULT_TIMEOUT_SECONDS;
  }

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

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || confirmOpen) return;
    if (!uiLocked) return;
    setUILock(false);
    showToast("処理ロックを解除しました。", "info");
  });

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

  function getStoredNumberFormat() {
    try {
      return normalizeNumberFormat(localStorage.getItem(NUMBER_FORMAT_KEY));
    } catch {
      return DEFAULT_NUMBER_FORMAT;
    }
  }

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

  window.showToast = showToast;
  window.setUILock = setUILock;
  window.setToastPosition = setToastPosition;
  window.setNumberFormat = setNumberFormat;
  window.postNavigate = postNavigate;
  window.safeFetch = safeFetch;
})();
