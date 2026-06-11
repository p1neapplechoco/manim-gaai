# Scene 6: Đánh Giá Định Lượng, Benchmark Và Tầm Nhìn Mở Rộng

## Overview
- **Topic**: ViP-LLaVA được đánh giá định lượng qua `Visual Prompt Understanding Benchmark`, các kết quả SoTA, ví dụ suy luận/OCR/toán trên ảnh trái cây, và các hướng phát triển như `Yo'LLaVA`, `Matryoshka Multimodal Models`, `Multimodal AI Agents`, `Robot Learning`.
- **Hook**: Nếu model hiểu được mũi tên, scribble, mask... thì ta đo năng lực đó như thế nào?
- **Target Audience**: Người học AI đã biết LLaVA/ViP-LLaVA ở mức khái niệm.
- **Estimated Length**: ~6-8 phút.
- **Key Insight**: ViP-LLaVA không chỉ demo tốt. Nó được kiểm tra bằng benchmark định lượng, cho thấy năng lực `recognition`, `counting`, `captioning`, `commonsense reasoning`, đồng thời mở ra hướng LMM cá nhân hóa và điều khiển độ chi tiết token hình ảnh.

## Asset Notes
- Asset user yêu cầu:
  - `Talk2/Image/Scene6/Vegetable.png`
  - `Talk2/Image/Scene6/Matryosha.png`
- Asset hiện có trong repo:
  - `Talk2/Image/Scene6/image.png`: ảnh `Matryoshka Multimodal Models`.
  - `Talk2/Image/Scene6/Matryosha.png`: ảnh sạp trái cây/rau củ có khung đỏ, xanh dương, xanh lá.
- Khi code, nên tạo path fallback:
  - `VEGETABLE_IMAGE = Scene6/Vegetable.png`; nếu không có thì dùng `Scene6/Matryosha.png`.
  - `MATRYOSHKA_IMAGE = Scene6/Matryosha.png`; nếu ảnh này là vegetable thì dùng fallback `Scene6/image.png`.

## Narrative Arc
Scene bắt đầu bằng câu hỏi: demo visual prompt nhìn rất thuyết phục, nhưng benchmark nói gì? Từ đó, video giới thiệu các kết quả SoTA trên bốn nhóm tác vụ, rồi zoom vào `Visual Prompt Understanding Benchmark` với 303 câu hỏi phức tạp. Sau ví dụ trái cây, video chuyển sang hai hướng mở rộng: cá nhân hóa với `Yo'LLaVA` và kiểm soát độ hạt token với `Matryoshka Multimodal Models`, trước khi kết lại bằng các giới hạn và tầm nhìn về agent/robot learning.

---

## Scene 1: Từ Demo Sang Đo Lường
**Duration**: ~45 giây  
**Purpose**: Mở đầu bằng câu hỏi đánh giá định lượng.

### Visual Elements
- Title lớn:
  `Quantitative Evaluation`
  dòng phụ: `Đánh giá định lượng`
- Các icon/khối nhỏ bay vào:
  `recognition`, `counting`, `captioning`, `visual reasoning`, `OCR`, `math`
- Một visual prompt màu vàng trên ảnh giả lập, biến thành biểu tượng thước đo/benchmark.
- Dòng hook:
  `Hiểu visual prompt không chỉ là demo. Nó cần được đo.`

### Content
Sau khi đã thấy ViP-LLaVA hiểu mũi tên, scribble và mask, câu hỏi tiếp theo là: năng lực này có ổn định trên nhiều dạng bài không? Câu trả lời đến từ benchmark định lượng.

### Narration Notes
"Một ví dụ đẹp có thể gây ấn tượng. Nhưng để biết model thật sự mạnh hay không, ta cần benchmark: nhiều câu hỏi, nhiều kiểu prompt, nhiều năng lực phải phối hợp cùng lúc."

### Technical Notes
- Dùng `Text`, `RoundedRectangle`, `Arrow`.
- Animate các capability chips tụ lại thành một bảng benchmark.
- Style nền tối, màu vàng cho visual prompt, xanh dương cho vision, xanh lá cho reasoning.

---

## Scene 2: SoTA Trên Nhiều Nhóm Tác Vụ
**Duration**: ~95 giây  
**Purpose**: Trình bày bảng kết quả định lượng và nhấn mạnh ViP-LLaVA đạt SoTA.

### Visual Elements
- Bốn bảng nhỏ đặt dạng 2x2 hoặc hàng ngang:

**Table 1: Object recognition in Visual7W**
| Method | Accuracy (%) |
|---|---:|
| 12in1 | 83.35 |
| GPT4ROI-7B | 81.83 |
| GPT4ROI-13B | 84.82 |
| Shikra-13B | 85.33 |
| Ours-13B | **87.91** |

**Table 2: Object counting in PointQA-LookTwice**
| Method | Accuracy (%) |
|---|---:|
| Point and ask | 60.20 |
| LLaVA-1.5-7B | 56.19 |
| LLaVA-1.5-13B | 57.93 |
| Shikra-13B | 70.30 |
| Ours-13B | **71.77** |

**Table 3: Visual Reasoning in VCR**
| Model | Q -> AR (%) |
|---|---:|
| ViLBERT | 54.0 |
| Unicode-VL | 54.5 |
| VLBERT-L | 58.9 |
| GPT4RoI-7B | 78.6 |
| Ours-7B | **78.93** |

**Table 4: Region Captioning in RefCOCOg**
| Model | METEOR | CIDEr |
|---|---:|---:|
| GRIT | 15.2 | 71.6 |
| Kosmos-2 | 14.1 | 62.3 |
| GLaMM | **16.2** | 105.0 |
| Ours-7B | **16.2** | **105.9** |

- Các ô `Ours` sáng lên bằng màu vàng/cam.
- Dòng summary:
  `SoTA on recognition, counting, captioning, and commonsense reasoning tasks`

### Content
ViP-LLaVA đạt kết quả tốt nhất hoặc đồng tốt nhất ở nhiều nhóm tác vụ:
- Object recognition: `87.91%`.
- Object counting: `71.77%`.
- Visual reasoning: `78.93%`.
- Region captioning: `16.2 METEOR`, `105.9 CIDEr`.

### Narration Notes
"Điểm đáng chú ý là các tác vụ này không giống nhau. Nhận dạng, đếm, suy luận và caption vùng ảnh đều kiểm tra những mặt khác nhau của hiểu hình ảnh có điều khiển."

### Technical Notes
- Có thể tái tạo bảng bằng rectangles/text thay vì dùng screenshot để animate từng ô.
- Nếu cần tiết kiệm thời gian, làm 4 table cards, chỉ hiện top/bottom rows và highlight `Ours`.
- Dùng `Circumscribe` lần lượt trên các ô `Ours`.

---

## Scene 3: Visual Prompt Understanding Benchmark
**Duration**: ~70 giây  
**Purpose**: Giới thiệu benchmark 303 câu hỏi phức tạp.

### Visual Elements
- Một counter lớn:
  `303 complex questions`
- Các capability nodes xung quanh:
  - `Perception / Nhận thức`
  - `OCR / Đọc chữ`
  - `World knowledge / Kiến thức chung`
  - `Math / Làm toán`
  - `Relation reasoning / Quan hệ đối tượng`
  - `Language generation / Sinh ngôn ngữ`
- Các node nối vào một câu hỏi trung tâm:
  `Visual Prompt Understanding`

### Content
Benchmark không chỉ hỏi model "vật gì đây?". Các câu hỏi yêu cầu kết hợp nhiều khả năng cùng lúc: nhìn đúng vùng được prompt, đọc chữ, hiểu mối quan hệ, làm toán đơn giản, và diễn đạt câu trả lời.

### Narration Notes
"Visual prompt làm câu hỏi cụ thể hơn về không gian. Nhưng để trả lời đúng, model vẫn phải dùng cả một chuỗi năng lực: nhìn, đọc, so sánh, suy luận và nói ra đáp án."

### Technical Notes
- Dùng graph/radial layout: node trung tâm và 6 node năng lực.
- Animate từng capability bằng `GrowFromCenter`, rồi nối line về benchmark.
- Counter `303` nên xuất hiện bằng `ChangeDecimalToValue` hoặc `ValueTracker` nếu muốn sinh động.

---

## Scene 4: Ví Dụ Trái Cây - OCR + Math + Visual Prompt
**Duration**: ~110 giây  
**Purpose**: Minh họa một câu hỏi benchmark bằng ảnh sạp trái cây.

### Visual Elements
- Asset chính:
  - Dự kiến: `Talk2/Image/Scene6/Vegetable.png`
  - Fallback hiện có: `Talk2/Image/Scene6/Matryosha.png` nếu đó là ảnh trái cây.
- Ảnh sạp trái cây đặt lớn ở giữa/trái.
- Các khung màu đỏ, xanh dương, xanh lá đã có trong ảnh được nhấn bằng outline phát sáng.
- Câu hỏi dạng card:
  `Trái cây trong ô màu nào có giá thấp nhất?`
- Ba mini cards cạnh ảnh:
  - `Red box`: đọc giá.
  - `Blue box`: đọc giá.
  - `Green box`: đọc giá.
- Một dòng suy luận:
  `OCR -> so sánh giá -> nhận dạng quả -> Orange`

### Content
Ảnh có nhiều loại trái cây và nhiều bảng giá. Model phải:
1. Xác định đúng các vùng được đánh dấu bằng màu.
2. Đọc chữ/số trên bảng giá trong từng vùng (`OCR`).
3. So sánh giá.
4. Nhận dạng loại quả trong vùng có giá thấp nhất.
5. Trả lời: `Orange / Quả cam`.

### Narration Notes
"Đây là một câu hỏi nhỏ nhưng không hề đơn giản. Nếu bỏ qua visual prompt, model có thể nhìn nhầm vùng. Nếu không OCR được, nó không biết giá. Nếu không so sánh được, nó không biết thấp nhất là cái nào."

### Technical Notes
- Nếu ảnh đã có khung màu, dùng `SurroundingRectangle`/`Rectangle` mờ để pulse đúng ba vùng.
- Có thể dùng `Indicate` cho từng vùng theo thứ tự đỏ -> xanh dương -> xanh lá.
- Kết quả cuối dùng `Text("Orange / Quả cam")` màu xanh lá hoặc vàng.
- Tránh đặt quá nhiều text lên ảnh; các bước suy luận nên nằm dưới ảnh bằng chips.

---

## Scene 5: Yo'LLaVA - LMM Cá Nhân Hóa
**Duration**: ~70 giây  
**Purpose**: Giới thiệu hướng mở rộng cá nhân hóa.

### Visual Elements
- Title:
  `Yo'LLaVA: Your Personalized LMM`
- Một ảnh nhóm người dạng placeholder hoặc card minh họa.
- Câu hỏi:
  `Bạn có thấy <thao> trong bức ảnh này không?`
- Visual prompt/identity token `<thao>` sáng lên.
- Đáp án dạng chat bubble:
  `Có. Thao đang mỉm cười và giơ tay chữ V trong bữa tiệc.`
- Khác biệt:
  `person` -> `<thao>`

### Content
Yo'LLaVA chuyển từ nhận diện đối tượng chung chung sang nhận diện cá nhân cụ thể theo yêu cầu người dùng. Thay vì trả lời "một người", model có thể gắn thông tin cá nhân hóa vào người mà user quan tâm.

### Narration Notes
"Với LMM cá nhân hóa, câu hỏi không còn dừng ở 'có người nào trong ảnh không?'. Nó có thể trở thành 'người tôi quan tâm có ở đây không, và họ đang làm gì?'."

### Technical Notes
- Nếu chưa có ảnh riêng, dựng minh họa bằng avatar circles và label `<thao>`.
- Dùng highlight quanh một avatar.
- Giữ tone cẩn trọng: cá nhân hóa cần quyền riêng tư và kiểm soát dữ liệu.

---

## Scene 6: Matryoshka Multimodal Models
**Duration**: ~95 giây  
**Purpose**: Giải thích ý tưởng điều khiển độ hạt token hình ảnh.

### Visual Elements
- Asset:
  - Dự kiến: `Talk2/Image/Scene6/Matryosha.png`
  - Fallback hiện có: `Talk2/Image/Scene6/image.png` nếu đó là ảnh Matryoshka.
- Ảnh Matryoshka Multimodal Models xuất hiện lớn.
- Overlay bằng các token strips có độ dài khác nhau:
  - ít token: `coarse / tổng quát`
  - nhiều token: `fine / chi tiết`
- Một slider:
  `Granularity Controller`
- Arrow đi vào `Large Language Model`.

### Content
Matryoshka Multimodal Models lấy cảm hứng từ búp bê Nga lồng nhau. Thay vì luôn đưa cùng một số lượng token hình ảnh vào LLM, hệ thống dùng `Granularity Controller` để chọn độ dài token phù hợp với câu hỏi. Câu hỏi đơn giản dùng ít token hơn; câu hỏi cần chi tiết dùng nhiều token hơn.

### Narration Notes
"Không phải câu hỏi nào cũng cần cùng một mức chi tiết. Nếu chỉ hỏi 'cảnh này là gì?', ta có thể dùng biểu diễn thô. Nếu hỏi chi tiết nhỏ, cần nhiều token hơn. Matryoshka biến độ chi tiết thành thứ có thể điều khiển."

### Technical Notes
- Dùng asset chính làm nền.
- Có thể dựng token bars bằng `Rectangle` và animate số lượng token tăng/giảm.
- Dùng `ValueTracker` cho slider nếu code.
- Thuật ngữ giữ English: `Granularity Controller`, `visual tokens`, `Large Language Model`.

---

## Scene 7: Looking Forward - Chưa Giải Quyết Xong
**Duration**: ~75 giây  
**Purpose**: Nêu giới hạn hiện tại và các câu hỏi mở.

### Visual Elements
- Title:
  `Looking Forward: Not quite solved`
- Ba warning cards:
  - `Hallucinations / ảo giác`
  - `Video understanding / hiểu video`
  - `Smaller performant models / model nhỏ nhưng mạnh`
- Bên dưới là nhóm câu hỏi mở:
  - `Vì sao OCR emergent?`
  - `LLM mạnh hơn ảnh hưởng VLM thế nào?`
  - `Instruction tuning làm thay đổi knowledge ra sao?`

### Content
Dù đạt nhiều tiến bộ, bài toán hiểu hình ảnh chưa hoàn thiện. Model vẫn có thể hallucinate, khó hiểu video dài/động, và cần tối ưu để nhỏ gọn hơn. Ngoài ra, vẫn cần hiểu sâu vì sao một số năng lực xuất hiện sau training và LLM ảnh hưởng đến năng lực đa phương thức như thế nào.

### Narration Notes
"SoTA không có nghĩa là bài toán đã xong. Nó chỉ nói rằng ta đang tiến nhanh. Phần khó tiếp theo là làm cho model đáng tin hơn, hiểu động hơn, và hiệu quả hơn."

### Technical Notes
- Dùng warning color `#FF6666` cho hạn chế.
- Các câu hỏi mở có thể xuất hiện như sticky notes hoặc orbiting questions.
- Không làm scene quá tiêu cực; kết bằng transition sang future directions.

---

## Scene 8: Tương Lai - Agent Và Robot Learning
**Duration**: ~90 giây  
**Purpose**: Mở rộng tầm nhìn ứng dụng.

### Visual Elements
- Hai cột lớn:

**Multimodal AI Agents**
- icon camera + LLM + tools.
- flow:
  `observe -> self-reflect -> plan -> call API/tool -> collaborate`

**Visual Prompting for Robot Learning**
- robot arm hoặc mobile robot dạng schematic.
- mũi tên trajectory trong không gian 3D.
- ví dụ:
  `đi vòng qua thùng rác`
  `vứt lon Coca-Cola vào thùng tái chế`

### Content
Tương lai không chỉ là hỏi-đáp trên ảnh. Multimodal agents có thể quan sát môi trường, tự phản tư, lập kế hoạch, gọi tool/API và phối hợp với agent khác. Trong robot learning, visual prompting như PIVOT cho phép AI hướng dẫn robot bằng các chỉ báo trực quan lặp lại trong không gian hành động.

### Narration Notes
"Khi model hiểu được chỉ thị hình ảnh, bước kế tiếp rất tự nhiên là hành động: không chỉ nói về ảnh, mà dùng ảnh để lập kế hoạch và điều khiển môi trường."

### Technical Notes
- Dùng diagram flow với arrow.
- Với robot, có thể vẽ path bằng `VMobject.set_points_smoothly`.
- Không cần 3D thật; 2D schematic đủ rõ.

---

## Scene 9: Kết Luận - Specialist Sang Generalist
**Duration**: ~70 giây  
**Purpose**: Kết video bằng thông điệp lớn.

### Visual Elements
- Bên trái:
  `Specialist models`
  nhiều model nhỏ riêng lẻ:
  `OCR`, `detection`, `captioning`, `VQA`, `robot policy`
- Bên phải:
  `Generalist multimodal model`
  một foundation model lớn nhận:
  `image + visual prompt + text + tools`
- Các mảnh từ bên trái transform vào mô hình bên phải.
- Dòng kết:
  `Foundation models + semi-automatic data -> controllable visual understanding`

### Content
Ngành đang dịch chuyển từ các mô hình chuyên gia đơn lẻ sang các mô hình đa phương thức tổng quát. Thành công đến từ foundation models mạnh, dữ liệu bán tự động, và cách thiết kế interaction giúp model hiểu các khái niệm mở trong thế giới thực.

### Narration Notes
"Điểm quan trọng không chỉ là một model mới. Đó là một hướng đi: biến hình ảnh, ngôn ngữ và hành động thành cùng một không gian tương tác có thể điều khiển."

### Technical Notes
- Dùng `ReplacementTransform` từ nhiều specialist cards sang one generalist card.
- Kết bằng `FadeIn` tagline và `Circumscribe`.

---

## Transitions & Flow
- Scene 1 -> 2: thước đo benchmark mở ra thành các bảng kết quả.
- Scene 2 -> 3: các số liệu co lại thành `Visual Prompt Understanding Benchmark`.
- Scene 3 -> 4: benchmark node biến thành ảnh trái cây cụ thể.
- Scene 4 -> 5: visual prompt trên trái cây chuyển thành identity prompt `<thao>`.
- Scene 5 -> 6: identity token biến thành visual token strip, mở ra Matryoshka.
- Scene 6 -> 7: token strip thu gọn thành dấu hỏi `Not quite solved`.
- Scene 7 -> 8: warning cards chuyển thành future direction cards.
- Scene 8 -> 9: agent/robot icons hòa vào generalist multimodal model.

## Color Palette
- **Background**: `#1C1C1C` - nền tối.
- **Visual / benchmark blue**: `#58C4DD` - vision, CLIP, OCR.
- **Reasoning green**: `#83C167` - reasoning, answer, agents.
- **Prompt yellow**: `#FFFF00` - visual prompt, benchmark highlight.
- **Projector orange**: `#FF8C2A` - Matryoshka, controller, transformations.
- **Warning red**: `#FF6666` - hallucination, limitations.

## Mathematical / Quantitative Content
- Các số liệu bảng:
  - Visual7W object recognition: `Ours-13B = 87.91%`.
  - PointQA-LookTwice object counting: `Ours-13B = 71.77%`.
  - VCR visual reasoning: `Ours-7B = 78.93%`.
  - RefCOCOg region captioning: `Ours-7B = 16.2 METEOR`, `105.9 CIDEr`.
- Benchmark size:
  - `303` complex questions.
- Công thức/flow gợi ý:
  ```latex
  \text{visual prompt} + \text{OCR} + \text{math} + \text{reasoning} \rightarrow \text{answer}
  ```
  ```latex
  \text{coarse tokens} \subset \text{fine tokens}
  ```

## Implementation Order
1. Tạo helper cho `card`, `image_card`, `table_card`, `capability_chip`.
2. Code Scene 2 trước vì bảng số liệu là phần nhiều layout nhất.
3. Code Scene 4 với asset trái cây; kiểm tra lại path vì hiện `Vegetable.png` chưa thấy trong repo.
4. Code Scene 6 với asset Matryoshka; kiểm tra lại path vì hiện `image.png` và `Matryosha.png` có vẻ đang bị đảo nội dung.
5. Code các scene còn lại bằng diagram/card/arrow.
6. Render thử từng cảnh bằng:
   `manim -ql -s Talk2/Src/Scene6_vi.py Scene6`

## Notes For Coding
- Nên dùng `TEXT_FONT = "Segoe UI"` để tiếng Việt không bị tách dấu.
- Với ảnh screenshot/bảng trắng, nếu đặt trên nền tối nên bọc trong frame màu trắng hoặc giảm sáng nền xung quanh.
- Không nhồi toàn bộ chữ của phần Looking Forward lên một màn hình. Chia thành cards ngắn, mỗi card 1 ý.
- Các thuật ngữ quan trọng giữ English:
  `Quantitative Evaluation`, `Visual Prompt Understanding Benchmark`, `SoTA`, `OCR`, `Visual Reasoning`, `Region Captioning`, `Yo'LLaVA`, `Matryoshka Multimodal Models`, `Granularity Controller`, `Multimodal AI Agents`, `Visual Prompting for Robot Learning`, `PIVOT`, `foundation models`, `generalist`.
