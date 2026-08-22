"""
FFA Python/CGI - プレイヤー掲示板 (bbs.py)
ログイン中のプレイヤーが自由に書き込める共有掲示板。
"""

import os

# 共通モジュールと設定モジュールのインポート
try:
    import config
    from sub_def import common
except ImportError:
    from . import config
    from sub_def import common


def main():
    # メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    params = common.decode_params()
    user_id = params.get("id", "").strip()
    # 認可: 掲示板は本人のIDでのみ利用（IDOR対策・ロック取得前にチェック）
    common.require_owner(user_id)

    mode = params.get("mode", "").strip()

    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクター情報が見つかりません。ログインし直してください。")

    # === 投稿処理 ===
    if mode == "post":
        message = params.get("message", "").strip()
        return_url = f"{config.Config['main_script']}&id={user_id}#ff-bbs"

        if not message:
            common.redirect_with_flash(return_url, "本文を入力してください。", "error")
        if len(message) > 200:
            common.redirect_with_flash(return_url, "本文は200文字以内で入力してください。", "error")

        # 禁止ワードチェック
        for word in config.Config['ban_words']:
            if word in message:
                common.redirect_with_flash(return_url, f"入力に禁止語「{word}」が含まれています。", "error")

        # 投稿の read-modify-write をアトミックにするための排他ロック。
        # bbs_load / bbs_regist は内部で "bbs" ロックを使うため、外側は別名 "bbs_post" を使う
        # (同名だと自己デッドロックする)。
        common.get_lock("bbs_post")
        try:
            posts = common.bbs_load()
            posts.insert(0, {
                "id": user_id,
                "name": chara.get("name", "名無し"),
                "img": chara.get("img", 0),
                "message": message,
                "time": common.get_time_str(),
                "host": os.environ.get("REMOTE_ADDR", "127.0.0.1"),
            })
            # 上限を超えた古い投稿は破棄
            if len(posts) > config.Config['bbs_storage_limit']:
                posts = posts[:config.Config['bbs_storage_limit']]
            common.bbs_regist(posts)
        finally:
            common.release_lock("bbs_post")

        # 投稿後は一覧へ戻す（再送信・二重投稿防止のためリダイレクト）
        common.redirect_with_flash(return_url, "掲示板に書き込みました。", "success")
        return

    # 掲示板は街に埋め込んで表示するため、単独ページは使わない。
    common.redirect(f"{config.Config['main_script']}&id={user_id}#ff-bbs")


if __name__ == "__main__":
    main()
