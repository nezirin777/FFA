"""
FFA Python/CGI - プレイヤー掲示板 (bbs.py)
ログイン中のプレイヤーが自由に書き込める共有掲示板。
"""

import os
import sys
import time

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

        if not message:
            common.show_error("本文を入力してください。")
        if len(message) > 200:
            common.show_error("本文は200文字以内で入力してください。")

        # 禁止ワードチェック
        for word in config.Config['ban_words']:
            if word in message:
                common.show_error(f"入力に禁止語「{word}」が含まれています。")

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
            if len(posts) > config.Config['max_bbs_posts']:
                posts = posts[:config.Config['max_bbs_posts']]
            common.bbs_regist(posts)
        finally:
            common.release_lock("bbs_post")

        # 投稿後は一覧へ戻す（再送信・二重投稿防止のためリダイレクト）
        from sub_def.utils import redirect
        redirect(f"{config.Config['bbs_script']}&id={user_id}")
        return

    # === 一覧表示 ===
    posts = common.bbs_load()
    context = {
        "chara": chara,
        "posts": posts,
        "chara_img": config.Config['chara_images'],
    }
    common.render_template("bbs.html", context)


if __name__ == "__main__":
    main()
