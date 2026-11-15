# maechan-reels ― インスタ @maechan_0616 リール自動制作キット

不動産売買仲介の店長（BOSS）のインスタ用リールを、毎日1本つくって20:00に投稿するための道具一式です。
作業するのは Claude（BOSSからは「大臣」と呼ばれる）。この README が作業手順書です。

- 目的：インスタから「家を買いたい」「家を売りたい」「ハウスメーカーを紹介して」の問い合わせを得る
- 目標：フォロワー1万人（2026年末）。2026/11/15 時点 454人
- 投稿：毎日1本・20:00（日本時間）
- 動画の公開URL：`https://raw.githubusercontent.com/0616yutom-dot/maechan-reels/main/videos/<ファイル名>.mp4`
  （だめなら `https://cdn.jsdelivr.net/gh/0616yutom-dot/maechan-reels@main/videos/<ファイル名>.mp4`）

## フォルダ
| 場所 | 中身 |
|---|---|
| `kit/lib.js` `kit/base.css` | アニメの共通部品（`render(t)` に秒を渡すとその瞬間の絵を描く方式） |
| `kit/capture.py` | HTMLを1コマずつ撮って mp4 にする（Playwright＋ffmpeg） |
| `kit/d.html` `kit/audio_d.py` | **見本①：知識系**「住宅ローン控除」29秒。家族の絵を全面に使う型。まずこれを写して作る |
| `kit/c.html` `kit/audio_c.py` | **見本②：悩み系**「静かにして！→解決策3つ」24秒。カード中心の型（絵は `kit/d/` の家族の絵に差し替えて使う） |
| `kit/d/` | 家族の絵（縦1140×2000に整えた10枚）と顔の丸アイコン5つ |
| `videos/` | 完成動画（`YYYY-MM-DD_ネタ名.mp4`。ファイル名は半角英数字とハイフンのみ） |
| `log/posts.md` | 投稿の記録と数字、学び。**毎回、最初に読み、最後に書き足す** |

## 家族の絵（`kit/d/`）の使い分け
| ファイル | 絵 | 向いている場面 |
|---|---|---|
| `rain.jpg` | 雨の中で見上げる（白黒） | 冒頭の「損・不安・知らないと危ない」 |
| `sun.jpg` | 光が差す空・ガッツポーズ | 「得する・戻る・解決」 |
| `gogo.jpg` | 家の前でキメ顔 | 「プロが教える」「決断」。※元絵の右上に漫画風の描き文字があるので、画面に入っていないか必ず静止画で確認し、入るなら使わない |
| `sunset.jpg` `sakura.jpg` | 大笑い | 保存の呼びかけ、明るい結末 |
| `think.jpg` | 山の上で考えるポーズ | 「〇〇ってなに？」の質問 |
| `sofa.jpg` | ソファ・スーツ・高級な室内 | 高級感、まとめ |
| `home.jpg` | 家の中で見上げる（大きな窓） | 家・間取り・制度の話 |
| `camp.jpg` | キャンプの焚き火 | 暮らし・休日・庭 |
| `back.jpg` | 夕日の後ろ姿 | しめの余韻、将来の話 |
| `papa.jpg` `mama.jpg` `ani.jpg` `baby.jpg` `neko.jpg` | 顔アイコン（パパ・ママ・長男・次男・猫） | 吹き出しでひと言 |

登場人物：パパ（宅建士。答える役）、ママ（驚く・共感する役）、長男（質問する役）、次男（「ここ大事！」など短いひと言）、猫。

## デザインの決まり（BOSSの承認済み）
- **高級感**：濃紺 `#101C2D`、金 `#C6A45B` / `#F3DFA0`、生成り `#F1E8D0`。見出しは明朝体（Noto Serif CJK JP）、説明と吹き出しはゴシック体。
- **最初の1秒で止める**：0秒の1コマ目から絵と大きな文字が読める状態で始める（黒い画面・無音で始めない）。1.5秒以内に絵を1回切り替える。
- 縦 1080×1920、30コマ/秒、長さ 20〜30秒。1画面1メッセージ、3秒以内に次の動き。
- 大事な文字は 上250px・下480px・右120px を避ける（インスタのボタンと重なる）。文字の帯は y=1020〜1450 が基本。
- 1行の文字幅は 1000px 以内。全角1文字 ≒ 文字サイズpx。例：10文字なら 100px まで。**必ず静止画で端が切れていないか確認**。
- 写真の上の金色文字（`.g`）は `text-shadow` を付けると消える。`.ts .g{text-shadow:none;filter:drop-shadow(...)}` を消さないこと（`d.html` に入っている）。
- 主役の数字は1本に1つ。数字はカウントアップで見せる。
- 最後は必ず「保存して」→「DMに2文字を送るだけ」＋ `@maechan_0616` フォローの呼びかけ。
- 音は自作（`audio_*.py`）。著作権のある曲・歌詞・キャラクター・他社の絵は使わない。

## 中身の決まり
- 配分：**悩み系4：知識系3**（1週間で）。`log/posts.md` を見て、かぶらないネタ・足りない方の型を選ぶ。
- 悩み系：賃貸や子育ての悩み →「こうすれば解決じゃね？」と解決策3つ（今すぐ／次の更新で／根本解決＝マイホーム）。
- 知識系：用語をタイトルにしない。「得する金額・損する場面」から入り、長男が「パパ、〇〇ってなに？」と聞き、パパが答える。
- むずかしい言葉は使わない。専門用語には必ずひと言説明を添える。
- **数字・制度・税金・金利は、毎回 WebSearch で最新を調べ直す**（国交省・国税庁・金融機関などの一次情報を優先）。確認できない数字は使わない。「最大」「〜の場合」「条件で変わります」の注意書きを動画と投稿文に入れる。
- 断定しすぎない（「絶対得」「必ず儲かる」は禁止）。持ち家が正解とは限らない、と正直に言うのは可。
- 特定の物件・他社・実在の人を出さない。誇大な表現、不安をあおりすぎる表現は避ける。
- 投稿文：1行目に動画のフックと同じ言葉 → 中身の要点 → 注意書き → 「DMに『◯◯』と送ってください📩」→ ハッシュタグ5個（うち1つは `#広島不動産`）。

## 作り方（1本ぶん）
```bash
cd kit
cp d.html new.html         # 知識系の見本を写す（悩み系は c.html の構成を参考に、絵は d/ を使う）
# new.html の <section> の文字・絵・秒数（data-a / data-b）と、下の render(t) 内の秒数をネタに合わせて書き換える
python3 capture.py new.html chk still 0,1.0,3.3,6.3,10.8,14.4,18.4,22.6,24.6,28.6   # 各場面の静止画 chk_<秒>.jpg を作り、Read で必ず目で確認
python3 capture.py new.html new video 0,1.3,3.7,6.7,11.1,14.7,18.7,22.9,24.9,29.0   # シーン境界の秒を並べる → new_silent.mp4
# 音：audio_d.py を写して DUR と効果音の秒数を場面に合わせ、出力名を new.wav に
python3 audio_new.py
ffmpeg -y -loglevel error -i new_silent.mp4 -i new.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart ../videos/YYYY-MM-DD_neta.mp4
```
- 直すときは、直した場面の番号だけ撮り直せる：`capture.py new.html new video <境界…> 2,5`
- `capture.py` は `/usr/bin/google-chrome` と Python の playwright を使う。無ければ `pip install playwright --break-system-packages && playwright install chromium` を入れ、`executable_path` の指定を外す。
- 日本語フォントは Noto Sans CJK JP / Noto Serif CJK JP。無ければ `fc-list | grep -i noto` で確認し、入っている日本語フォントに置き換える。
- 作業中にできる `*_seg*.mp4` `*_silent.mp4` `*.wav` `chk*.jpg` `new*.html` などは push しない（`.gitignore` 済み）。push するのは `videos/` の完成動画と `log/` だけ。

## 投稿のしかた
1. 完成動画を `videos/` に入れて `main` に push。
2. `curl -sI <公開URL>` で 200 が返るのを確認（反映に1分ほどかかることがある）。
3. Windsor.ai のインスタ連携で投稿：connector=`instagram`、account=`17841469026505231`、action=`create_video_post`、params=`{"video_url": 公開URL, "caption": 投稿文, "share_to_feed": true}`。
4. 失敗したら jsDelivr のURLでもう1回だけ試す。それでもだめなら動画と投稿文をBOSSに届け、手動投稿をお願いする。**同じ動画を2回投稿しないこと**（投稿できたか不明なときは、先に Windsor の get_data で当日の投稿を確認する）。

## 分析のしかた
- Windsor `get_data`（connector=`instagram`、`date_preset`=`last_7dT`。無料お試し中は直近30日まで）で、
  `timestamp, media_caption, media_views, media_reach, media_like_count, media_saved, media_shares, media_comments_count, media_reel_avg_watch_time, media_reel_skip_rate` と、`followers_count` を取る。
- 見方：3秒で飛ばされる割合が高い→冒頭を変える／見られた秒数が短い→短く・切り替えを速く／シェア・保存が少ない→ネタを変える。
- 気づきは `log/posts.md` の「学び」に1〜2行で書き足し、次のネタ選びと冒頭づくりに使う。
