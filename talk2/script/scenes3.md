# LLaVA: Lam Sao Mot LLM Co The Nhin Thay Hinh Anh?


## Scene 1: Cau Hoi Mo Dau - LLM Nhin Anh Bang Cach Nao?
**Duration**: ~45 giay
**Purpose**: Dat van de va tao su to mo.

### Visual Elements
- Ben trai: mot hinh anh minh hoa don gian, vi du mot ban phong co vat the bat thuong.
- Ben phai: mot hop den co nhan "LLM" chi nhan cac token chu.
- Giua man hinh: cau hoi `What is unusual about this image?` tach thanh cac token nho.
- Dau hoi lon o trung tam: "Image -> ? -> Language".
- Mau sac: anh/thi giac mau blue, van ban mau green, dau hoi mau yellow.

### Content
Mo canh bang viec dua mot buc anh vao LLM. Anh bi chan lai o cong vao vi LLM chi chap nhan chuoi token ngon ngu. Cau hoi van ban di qua duoc, nhung hinh anh thi khong. Man hinh tam dung o khoang trong giua anh va LLM.

### Narration Notes
Giong mo dau nen gan gui: "Neu LLM chi biet doc chu, thi LLaVA da lam gi de no tra loi duoc ve mot buc anh?" Nhan manh rang bai toan khong phai chi la gan them camera, ma la noi hai khong gian bieu dien khac nhau.

### Technical Notes
- Dung `ImageMobject` hoac hinh placeholder bang `Rectangle` neu chua co asset.
- Dung `Text`, `MathTex`, `Arrow`, `VGroup`.
- Nen animate token van ban di vao LLM, con hinh anh bi dung lai bang mot barrier/lock nho.

---

## Scene 2: Ban Do Tong The Cua LLaVA
**Duration**: ~60 giay
**Purpose**: Gioi thieu pipeline tong quat truoc khi di vao cong thuc.

### Visual Elements
- Pipeline trai sang phai:
  1. `Image X_v`
  2. `Vision Encoder g_theta`
  3. `Visual features Z_v`
  4. `Projection W / MLP`
  5. `Visual tokens H_v`
  6. `LLM f_phi`
  7. `Answer X_a`
- Duoi pipeline: text instruction `X_q`.
- Mui ten tu `X_q` vao LLM sau khi duoc bien thanh `H_q`.
- Nhan nho: "CLIP-ViT-L/14" duoi Vision Encoder, "Vicuna / LLaMA / MPT" duoi LLM.

### Content
Dat tat ca thanh phan len man hinh nhu mot so do he thong. Chua giai thich tung cong thuc, chi cho nguoi xem thay LLaVA co ba khoi quan trong: nhin anh, chieu sang khong gian ngon ngu, va sinh cau tra loi.

### Narration Notes
"Day la toan bo cau truc o muc cao. Anh di qua CLIP de thanh vector dac trung. Mot projector hoc cach dich vector do sang ngon ngu cua LLM. Sau do LLM nhan ca token anh lan token cau hoi."

### Technical Notes
- Dung layout trai sang phai, cac khoi la `RoundedRectangle` nhe hoac `Rectangle`.
- Dung mau co y nghia nhat quan: visual blue, connector yellow, language green.
- Can de du khoang trong de Scene 3-5 zoom vao tung khoi.

---

## Scene 3: Vision Encoder - Bien Anh Thanh Dac Trung
**Duration**: ~70 giay
**Purpose**: Giai thich dau vao anh `X_v` va dac trung hinh anh `Z_v`.

### Visual Elements
- Anh `X_v` duoc cat thanh cac patch nho nhu luoi ViT.
- Cac patch chay vao khoi `CLIP-ViT-L/14`.
- Dau ra la mot day vector/dot/token mau blue, nhan `Z_v`.
- Cong thuc hien o duoi:
  `Z_v = g_\theta(X_v)`
- Mot o nho ghi "frozen" gan Vision Encoder.

### Content
Hinh anh khong di thang vao LLM. Dau tien no duoc chia thanh cac patch, ma hoa boi CLIP-ViT-L/14 da duoc tien huan luyen. Dau ra `Z_v` la tap cac dac trung hinh anh: nhung vector ma CLIP da hoc de bieu dien noi dung thi giac.

### Narration Notes
Nhan manh CLIP da co san nang luc noi anh voi mo ta van ban o muc dac trung, nen LLaVA tan dung no thay vi huan luyen vision encoder tu dau.

### Technical Notes
- Co the tao luoi patch bang `VGroup` cac `Square`.
- Dung `Transform` de bien patch thanh cac vector/doc bar.
- `g_\theta` nen hien nhu mot ham, nhung ghi chu rang trong training LLaVA goc, `theta` duoc giu dong bang.

---

## Scene 4: Projector - Cau Noi Giua Hai Khong Gian
**Duration**: ~90 giay
**Purpose**: Lam ro "aha moment": projector chieu visual features vao khong gian embedding cua LLM.

### Visual Elements
- Ben trai: dam may vector blue `Z_v` trong "visual space".
- Ben phai: dam may token green trong "language embedding space".
- O giua: ma tran/lop `W`, sau do bien hinh thanh `MLP` de ghi chu LLaVA-1.5.
- Mui ten bien doi:
  `H_v = W Z_v`
- Hien them:
  `H_v = MLP(Z_v)` voi nhan "LLaVA-1.5".
- Cac token visual sau chieu co dang giong token ngon ngu, nhung mau blue-green.

### Content
Projector la bo phien dich. Trong LLaVA ban dau, no co the hieu la mot linear layer voi ma tran trong so `W`. No nhan `Z_v` va tao ra `H_v`, cac visual token nam trong cung khong gian voi embedding cua LLM. O LLaVA-1.5, projector duoc nang cap thanh MLP de tang kha nang anh xa phi tuyen.

### Narration Notes
"Day la diem then chot: LLM khong can thay pixel. No chi can nhan mot day vector nam dung dinh dang ma no biet xu ly." Nen dung hinh anh "phien dich ngon ngu" nhung tranh lam no qua tre con.

### Technical Notes
- Dung hai `NumberPlane` hoac hai vung toa do 2D gia lap.
- Animate cac dot blue di qua `W` va canh hang voi dot green.
- Neu viet code ManimCE, dung `MathTex(r"H_v = W Z_v")`; neu ManimGL, dung `Tex(R"H_v = W Z_v")`.

---

## Scene 5: Instruction - Cau Hoi Cung Tro Thanh Embedding
**Duration**: ~60 giay
**Purpose**: Dua thanh phan ngon ngu `X_q -> H_q` vao cung pipeline.

### Visual Elements
- Cau hoi `X_q`: "What is unusual about this image?"
- Cau hoi tach thanh token: `[What] [is] [unusual] ...`
- Moi token bien thanh vector green `H_q`.
- Cong thuc:
  `H_q = Emb(X_q)`
- `H_v` va `H_q` duoc ghep thanh mot chuoi dau vao cho LLM:
  `[H_v ; H_q]`

### Content
Van ban cua nguoi dung cung duoc token hoa va embedding hoa nhu trong LLM thong thuong. Diem moi la chuoi dau vao bay gio khong chi co token chu, ma co them visual token o dau hoac o vi tri anh duoc chen vao prompt.

### Narration Notes
Nen noi ro: `H_v` khong phai chu viet, nhung voi LLM no co cung "dinh dang vector" voi token embedding. Vi vay ta co the noi chuoi nay la mot cau hoi da duoc gan them boi canh thi giac.

### Technical Notes
- Dung `TransformMatchingTex`/`ReplacementTransform` cho `X_q -> H_q`.
- Dung bracket hoac conveyor belt de ghep `[H_v ; H_q]`.

---

## Scene 6: LLM Sinh Cau Tra Loi
**Duration**: ~75 giay
**Purpose**: Giai thich output `X_a` va xac suat sinh token.

### Visual Elements
- Khoi LLM `f_\phi` nhan chuoi `[H_v ; H_q]`.
- Dau ra tung token mot: `[The] [unusual] [thing] [is] ...`
- Cong thuc hien dan:
  `X_a = f_\phi(H_v, H_q)`
  sau do chi tiet hon:
  `p(X_a | X_v, X_q) = \prod_t p_\phi(x_t | H_v, H_q, x_{<t})`
- Mot thanh xac suat nho chon token tiep theo.

### Content
Sau khi nhan du boi canh anh va cau hoi, LLM lam viec quen thuoc: du doan token tiep theo lap di lap lai. Ket qua la cau tra loi `X_a`. LLaVA vi the la mot VLM nhung phan sinh ngon ngu van nam trong co che autoregressive cua LLM.

### Narration Notes
"O thoi diem nay, magic da gan nhu bien mat. Moi thu quay lai bai toan quen thuoc: dua context vao, roi du doan token tiep theo."

### Technical Notes
- Dung `LaggedStart` de token output xuat hien lan luot.
- Cong thuc tich xac suat nen xuat hien sau cong thuc ngan de tranh qua tai.

---

## Scene 7: Training Stage 1 - Hoc Can Chinh Dac Trung
**Duration**: ~95 giay
**Purpose**: Giai thich giai doan tien huan luyen projector.

### Visual Elements
- Pipeline LLaVA quay lai, nhung Vision Encoder va LLM bi khoa bang icon "frozen".
- Projector `W` phat sang mau yellow va co nhan "trainable".
- Dataset minh hoa: nhieu cap `image-caption`, nhan "CC3M subset ~595K".
- Caption di vao nhu cau tra loi muc tieu.
- Loss hien o duoi:
  `\mathcal{L}_{align} = -\sum_t \log p_\phi(y_t | H_v, y_{<t})`

### Content
Giai doan 1 dung cac cap anh-van ban de day projector noi dung anh nen duoc dat vao khong gian LLM nhu the nao. Vision Encoder va LLM duoc dong bang; chi `W` duoc cap nhat. Muc tieu khong phai day LLM hoi dap phuc tap, ma la can chinh "ngon ngu vector" giua CLIP va LLM.

### Narration Notes
Nhan manh day la buoc can chinh. Neu bo qua buoc nay, visual token co the di vao LLM nhu mot ngon ngu la: dung dinh dang vector nhung sai phan bo, sai y nghia.

### Technical Notes
- Dung icon lock bang `Text("frozen")` hoac hinh khoa don gian.
- Animate gradient/update chi chay vao projector, khong chay vao hai khoi con lai.
- Co the dung mau red nhe cho gradient bi chan lai o Vision Encoder/LLM.

---

## Scene 8: Training Stage 2 - Visual Instruction Tuning
**Duration**: ~110 giay
**Purpose**: Giai thich cach LLaVA hoc tra loi chi thi mo.

### Visual Elements
- Dataset ba thanh phan: `Image`, `Instruction`, `Answer`.
- Nhan dataset: `LLaVA-Instruct-158K`.
- Ba loai task hien nhu ba cot:
  1. Conversation
  2. Detailed description
  3. Complex reasoning
- Vision Encoder van co khoa "frozen".
- Projector `W/MLP` va LLM `f_\phi` deu phat sang "trainable".
- Cong thuc loss tong quat:
  `\mathcal{L}_{inst} = -\sum_t \log p_\phi(x^a_t | H_v, H_q, x^a_{<t})`

### Content
Giai doan 2 day mo hinh lam tro ly thi giac. Du lieu khong chi la caption, ma la cac mau hoi dap da chuyen thanh dang instruction-following: mo ta chi tiet, hoi thoai, suy luan. Vision Encoder van dong bang de giu dac trung on dinh, con projector va LLM duoc tinh chinh de hoc cach dung thong tin thi giac khi tra loi.

### Narration Notes
"Stage 1 day mot ngon ngu chung. Stage 2 day cach noi chuyen bang ngon ngu do." Cau nay co the la nhan nho chot cua scene.

### Technical Notes
- Dung `Table` hoac ba `VGroup` card don gian cho dataset triplet.
- Neu muon giong 3b1b, transform cac cap image-caption cua Scene 7 thanh triplet image-instruction-answer.

---

## Scene 9: Dong Bang Va Mo Khoa - Ai Duoc Hoc O Moi Giai Doan?
**Duration**: ~60 giay
**Purpose**: Tom tat training bang mot bang so sanh de nguoi xem khong nham lan.

### Visual Elements
- Bang 2 hang:
  - Stage 1: Vision Encoder frozen, Projector trainable, LLM frozen.
  - Stage 2: Vision Encoder frozen, Projector trainable, LLM trainable.
- Moi cot la mot module trong pipeline.
- Icon lock/unlock theo tung o.

### Content
Scene nay lam ro trang thai tham so. No cung sua hieu lam pho bien: LLaVA khong nhat thiet huan luyen lai tat ca moi thu tu dau. Suc manh den tu viec tan dung CLIP va LLM co san, roi hoc cau noi va tinh chinh theo instruction.

### Narration Notes
Nen noi cham hon mot chut, vi day la phan de nham. "Khac biet lon nhat giua hai giai doan nam o viec LLM co duoc mo khoa hay khong."

### Technical Notes
- Dung `MobjectTable` trong ManimCE hoac custom `VGroup` rectangles de de style.
- Giu mau consistent voi pipeline: blue/vision, yellow/projector, green/LLM.

---

## Scene 10: Aha Moment - Anh Tro Thanh Mot Phan Cua Prompt
**Duration**: ~75 giay
**Purpose**: Ket noi truc giac voi cong thuc va chot insight.

### Visual Elements
- Prompt cuoi cung duoc hien nhu mot chuoi:
  `[visual tokens H_v] + [question tokens H_q] -> [answer X_a]`
- Visual tokens co texture/hinh nho ben trong, question tokens co chu, nhung tat ca nam tren cung mot dong embedding.
- Pipeline thu gon thanh mot cong thuc lon:
  `X_a \sim f_\phi([W g_\theta(X_v); Emb(X_q)])`
- Neu muon nhac LLaVA-1.5:
  `W` co the thay bang `MLP`.

### Content
Tat ca cac thanh phan gom lai thanh mot y tuong: anh duoc ma hoa, chieu vao khong gian ngon ngu, ghep voi instruction, roi LLM sinh cau tra loi. Day la cach LLaVA bien bai toan "may nhin" thanh bai toan "LLM doc mot prompt da co them token hinh anh".

### Narration Notes
Day la khoanh khac "aha". Nhan manh mot cau ngan: "LLaVA khong bien LLM thanh camera; LLaVA bien anh thanh mot phan cua prompt."

### Technical Notes
- Dung `FlashAround` hoac `Circumscribe` cho cong thuc cuoi.
- Neu video co nhac/beat, day la diem nen co pause 1 giay sau cau chot.

---

## Scene 11: Recap - Ba Cau Hoi Can Nho
**Duration**: ~50 giay
**Purpose**: Ket thuc gon, giup nguoi xem ghi nho.

### Visual Elements
- Ba dong recap hien lan luot:
  1. `What sees?` -> `CLIP-ViT-L/14`
  2. `What translates?` -> `Projection W / MLP`
  3. `What answers?` -> `LLM f_\phi`
- Duoi cung: "Vision Encoder + Projector + LLM = Visual Assistant".

### Content
Tong ket vai tro cua tung module va hai giai doan huan luyen. Co the ket bang viec quay lai hinh anh mo dau, lan nay cau hoi duoc tra loi tron ven.

### Narration Notes
Ket thuc bang giong chac chan: "Mot khi nam duoc cau noi nay, nhieu mo hinh vision-language hien dai se tro nen de doc hon rat nhieu."

### Technical Notes
- Co the tai su dung cac mobject tu Scene 2 de tao cam giac dong vong.
- Output answer cuoi co the chay bang `Write`/`AddTextLetterByLetter`.

---

## Transitions & Flow

### Scene Connections
- Scene 1 -> Scene 2: Khoang trong `Image -> ? -> Language` duoc mo rong thanh pipeline day du.
- Scene 2 -> Scene 3: Camera zoom vao Vision Encoder.
- Scene 3 -> Scene 4: Cac vector `Z_v` tu Vision Encoder bay sang projector.
- Scene 4 -> Scene 5: `H_v` sau khi chieu dung lai, `H_q` tu instruction duoc ghep vao ben canh.
- Scene 5 -> Scene 6: Chuoi `[H_v ; H_q]` di vao LLM va sinh `X_a`.
- Scene 6 -> Scene 7: Chuyen tu inference sang cau hoi "lam sao hoc duoc mapping nay?"
- Scene 7 -> Scene 8: Dataset image-caption bien thanh dataset image-instruction-answer.
- Scene 8 -> Scene 9: Pipeline dong lai thanh bang trang thai frozen/trainable.
- Scene 9 -> Scene 10: Bang tan bien, cong thuc tong hop hien len.
- Scene 10 -> Scene 11: Cong thuc thu gon thanh ba cau hoi recap.

### Recurring Visual Motifs
- **Blue**: thong tin thi giac, image patches, `Z_v`.
- **Yellow**: projector/cau noi/phan dang hoc.
- **Green**: ngon ngu, instruction, response, LLM.
- **Lock icon**: module frozen.
- **Conveyor belt/token stream**: chuoi dau vao cua LLM.

---

## Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Visual Primary | Blue | `#58C4DD` | Image, patches, visual features `Z_v` |
| Language Primary | Green | `#83C167` | Text tokens, `H_q`, answer `X_a`, LLM |
| Connector Accent | Yellow | `#FFFF00` | Projection `W`, MLP, key highlight |
| Frozen/Inactive | Gray | `#888888` | Frozen modules, background details |
| Warning/Blocked | Red | `#FF6666` | Barrier in opening, stopped gradients |
| Background | Dark gray | `#1C1C1C` | Main scene background |

---

## Mathematical Content

### Equations to Render
1. `Z_v = g_\theta(X_v)` - Scene 3, vision encoder.
2. `H_v = W Z_v` - Scene 4, original linear projection.
3. `H_v = MLP(Z_v)` - Scene 4, LLaVA-1.5 projector note.
4. `H_q = Emb(X_q)` - Scene 5, language instruction embedding.
5. `[H_v ; H_q]` - Scene 5, concatenated multimodal context.
6. `X_a = f_\phi(H_v, H_q)` - Scene 6, short response equation.
7. `p(X_a | X_v, X_q) = \prod_t p_\phi(x_t | H_v, H_q, x_{<t})` - Scene 6, autoregressive generation.
8. `\mathcal{L}_{align} = -\sum_t \log p_\phi(y_t | H_v, y_{<t})` - Scene 7, feature alignment objective.
9. `\mathcal{L}_{inst} = -\sum_t \log p_\phi(x^a_t | H_v, H_q, x^a_{<t})` - Scene 8, instruction tuning objective.
10. `X_a \sim f_\phi([W g_\theta(X_v); Emb(X_q)])` - Scene 10, final compact view.

### Tables
1. Training status table:
   - Stage 1: Vision Encoder frozen, Projection trainable, LLM frozen.
   - Stage 2: Vision Encoder frozen, Projection trainable, LLM trainable.
2. Dataset table:
   - Stage 1: CC3M subset, image-caption pairs, about 595K.
   - Stage 2: LLaVA-Instruct-158K, image-instruction-answer triplets.

### Geometric Objects
1. Patch grid over image: represents ViT tokenization.
2. Vector clouds: represent embedding spaces.
3. Projection bridge: represents `W`/MLP mapping visual features into LLM embedding space.
4. Token stream: represents concatenated multimodal prompt.

---

## Implementation Order

1. **Scene 2: Ban Do Tong The** - Build shared pipeline components first because many later scenes reuse them.
2. **Scene 3: Vision Encoder** - Implement patch grid and `Z_v` token output.
3. **Scene 4: Projector** - Implement vector-space transform and formulas.
4. **Scene 5-6: Instruction + LLM Output** - Implement token streams and autoregressive answer animation.
5. **Scene 7-9: Training** - Reuse pipeline, add lock/trainable states and dataset tables.
6. **Scene 1: Hook** - Implement after pipeline exists so opening can transition smoothly into overview.
7. **Scene 10-11: Aha + Recap** - Reuse all motifs and polish final timing.

### Shared Components
- `make_pipeline()` - creates Vision Encoder, Projector, LLM, arrows, labels.
- `make_token_stream(tokens, color)` - creates visual/text tokens with stable spacing.
- `make_lock_label(module, text="frozen")` - lock/frozen overlay.
- `make_dataset_triplet()` - image/instruction/answer card for Stage 2.
- `formula_style()` - consistent font size, color highlights, and bottom placement.

---

## Open Questions / Decisions Needed

- [ ] Video nen dung ManimCE (`from manim import *`) hay ManimGL/3b1b (`from manimlib import *`)? Kich ban nay dung duoc cho ca hai, nhung code se khac.
- [ ] Co can dung anh minh hoa that hay chi dung placeholder/toy image? Neu muon video dep hon, nen dung 1-2 anh minh hoa that cho hook va recap.
- [ ] Muc tieu video la giai thich cho nguoi hoc AI co ban hay cho nguoi da doc paper? Neu cho nguoi da doc paper, co the them chi tiet ve data generation bang GPT-4 va ablation LLaVA-1.5.

---

## Reference Material

- LLaVA project page: https://llava-vl.github.io/
- Visual Instruction Tuning paper: https://arxiv.org/abs/2304.08485
- Microsoft Research LLaVA overview: https://www.microsoft.com/en-us/research/project/llava-large-language-and-vision-assistant/
- LLaVA-1.5 overview/source pointers: https://mm-llms.github.io/posts/LLaVA-15/
