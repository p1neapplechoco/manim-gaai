# Scene 4: Khả Năng Của LLaVA - Từ Phản Hồi Chi Tiết Đến Benchmark

## Overview
- **Topic**: Khả năng phản hồi mạnh mẽ của LLaVA qua ví dụ ảnh lạ, hiểu parody/reference, và kết quả benchmark.
- **Hook**: Cùng một bức ảnh và cùng một câu hỏi, vì sao LLaVA trả lời sâu hơn các model khác?
- **Target Audience**: Người học AI đã biết LLM/VLM ở mức cơ bản.
- **Estimated Length**: ~5-7 phút.
- **Key Insight**: LLaVA không chỉ caption ảnh. Nó dùng ảnh như context để làm theo instruction, suy luận về tình huống, nhận ra điểm bất thường, và giải thích bằng ngôn ngữ tự nhiên.

## Narrative Arc
Video bắt đầu bằng ảnh `Yellow.png`: một tình huống rất lạ, nhưng câu hỏi lại đơn giản: "What is unusual about this image?" Từ đó, các model khác nhau được đặt cạnh nhau để thấy LLaVA trả lời chi tiết nhất. Sau ví dụ trực quan, video chuyển sang một ví dụ hiểu reference văn hóa với Mona Lisa parody, rồi kết thúc bằng benchmark: bảng LLaVA-1.6-34B và radar chart LLaVA-1.5.

---

## Scene 1: Một Bức Ảnh, Một Câu Hỏi
**Duration**: ~45 giây
**Purpose**: Tạo hook bằng ảnh `Yellow.png` và câu hỏi chung cho mọi model.

### Visual Elements
- Ảnh `Yellow.png` đặt lớn ở giữa màn hình.
- Câu hỏi xuất hiện phía dưới ảnh:
  `What is unusual about this image?`
- Một hàng 4 model nằm dưới dạng tab hoặc avatar:
  `LLaVA`, `GPT-4`, `BLIP-2`, `OpenFlamingo`
- Camera zoom nhẹ vào vùng người đang là quần áo trên xe.

### Content
Người xem thấy một ảnh rất lạ: một người đang là quần áo trên phía sau/nóc một chiếc xe màu vàng. Câu hỏi không yêu cầu nhận diện object đơn giản, mà yêu cầu hiểu điều gì "unusual".

### Narration Notes
"Nếu chỉ nhìn thấy xe, người, đường phố, thì model mới chỉ caption ảnh. Nhưng câu hỏi này đòi hỏi nhiều hơn: phải hiểu hành động, bối cảnh, và điều gì lệch khỏi đời thường."

### Technical Notes
- Asset chính: `image/scene4/Yellow.png`. Nếu code trong repo hiện tại, có thể dùng path đã thấy: `media/images/Scene4_vi/Yellow.png`.
- Dùng `ImageMobject`.
- Dùng `SurroundingRectangle` hoặc `Rectangle` stroke đỏ để highlight khu vực người và bàn là.
- Câu hỏi dùng `Text`, không cần LaTeX.

---

## Scene 2: LLaVA Trả Lời Kĩ Nhất
**Duration**: ~85 giây
**Purpose**: So sánh trực tiếp câu trả lời của các model cho cùng một ảnh/câu hỏi.

### Visual Elements
- Màn hình chia thành 4 response cards:
  1. `LLaVA`
  2. `GPT-4 [32]`
  3. `BLIP-2`
  4. `OpenFlamingo`
- Card LLaVA lớn hơn, sáng hơn, màu xanh lá.
- Các card còn lại nhỏ hơn hoặc xếp bên dưới.
- Dùng highlight đỏ cho các cụm quan trọng trong LLaVA response:
  - `man ironing clothes`
  - `on the back of a minivan or van`
  - `unsafe and unconventional`
  - `maintain balance and stability`

### Content
Các câu trả lời hiển thị theo thứ tự:

**LLaVA**
"The unusual aspect of this image is a man ironing clothes on the back of a minivan or van. This is not a typical place to perform this activity, as one would usually iron clothes in a more stationary and safe location, such as a home, using a regular ironing board. The scene depicted in the image is peculiar as it involves a makeshift ironing setup on a vehicle, which can be both unsafe and unconventional. Additionally, it is not clear how the man is able to maintain balance and stability while ironing clothes in such an unstable environment."

**GPT-4 [32]**
"The unusual thing about this image is that a man is ironing clothes on an ironing board attached to the roof of a moving taxi."

**BLIP-2**
"a man is sitting on the back of a yellow cab"

**OpenFlamingo**
"The man is drying his clothes on the hood of his car."

### Narration Notes
"Điểm đáng chú ý không phải chỉ là LLaVA đoán đúng. Nó còn giải thích vì sao chuyện đó lạ: hoạt động là ironing, vị trí là trên xe, và bối cảnh này vừa không an toàn vừa không thông thường."

### Technical Notes
- Với response dài của LLaVA, không cần show toàn bộ cùng lúc. Nên type từng đoạn:
  1. Nhận ra hành động.
  2. Nhận ra vị trí.
  3. So với bối cảnh bình thường.
  4. Kết luận unsafe/unconventional.
- Dùng `AddTextLetterByLetter` hoặc `Write` theo từng dòng.
- Có thể làm LLaVA card rộng 6.5, các card còn lại rộng 3-4.

---

## Scene 3: Vì Sao Câu Trả Lời Của LLaVA Mạnh?
**Duration**: ~65 giây
**Purpose**: Phân tích response của LLaVA thành các lớp reasoning.

### Visual Elements
- Response LLaVA co lại thành 4 khối logic nối bằng arrow:
  1. `Visual perception`: thấy người, xe, bàn là.
  2. `Action recognition`: đang ironing.
  3. `Commonsense`: ironing thường diễn ra ở nơi ổn định/an toàn.
  4. `Visual reasoning`: tình huống này unusual, unsafe, unconventional.
- Ảnh `Yellow.png` ở bên trái, các khối reasoning ở bên phải.
- Dòng kết luận lớn:
  `Captioning -> Reasoning`

### Content
LLaVA không chỉ liệt kê object. Nó kết nối object với hành động, hành động với bối cảnh đời thường, rồi suy ra điều bất thường.

### Narration Notes
"Một câu trả lời tốt đi qua nhiều tầng. Tầng thấp là nhìn thấy vật thể. Tầng cao hơn là hiểu hành động. Tầng cuối là so với thế giới bình thường để phát hiện cái lạ."

### Technical Notes
- Dùng các card màu:
  - Visual blue: perception.
  - Yellow: commonsense bridge.
  - Green: reasoning/answer.
- Animate từng khối bằng `FadeIn` + `GrowArrow`.

---

## Scene 4: Khả Năng Hiểu Parody - Mona Lisa
**Duration**: ~75 giây
**Purpose**: Cho thấy LLaVA có thể hiểu reference văn hóa và mục đích nghệ thuật/hài hước.

### Visual Elements
- Ảnh Mona Lisa parody đặt bên trái.
- Câu hỏi phía trên hoặc trong chat bubble:
  `What may be the purpose of this painting?`
- Bên phải là response của LLaVA, chia thành các ý:
  - `famous painting: The Mona Lisa`
  - `dog in the same pose`
  - `creative and humorous take`
  - `tribute / cultural commentary`
- Highlight hai ý quan trọng:
  - `dog in the same pose as the Mona Lisa`
  - `creative and humorous take`

### Content
Response cần thể hiện đầy đủ ý:
"The purpose of this painting could be to create an artistic representation of the famous painting, 'The Mona Lisa,' by Leonardo da Vinci. The artist has painted a dog in the same pose as the Mona Lisa, wearing a mask, and standing in front of a backdrop that resembles the original painting. This artistic interpretation may serve as a creative and humorous take on the iconic painting, drawing attention to the dog's unique expression and the contrast between the dog's appearance and the original subject. The painting could also be a tribute to the original work or a commentary on the cultural significance of the Mona Lisa."

### Narration Notes
"Ở ví dụ này, model không chỉ nhìn thấy một con chó. Nó nhận ra reference tới Mona Lisa, hiểu sự thay thế nhân vật, rồi suy ra mục đích: parody, humor, hoặc commentary."

### Technical Notes
- Asset Mona Lisa: nếu dùng repo hiện tại, có thể dùng `media/images/Scene4_vi/Monalisa.png`.
- Có thể đặt một outline mờ phía sau ảnh để gợi pose Mona Lisa.
- Thuật ngữ quan trọng giữ English: `reference`, `parody`, `world knowledge`, `visual reasoning`.

---

## Scene 5: Từ Ví Dụ Sang Benchmark
**Duration**: ~45 giây
**Purpose**: Chuyển từ hai ví dụ định tính sang câu hỏi định lượng: benchmark nói gì?

### Visual Elements
- Hai ví dụ trước thu nhỏ thành 2 thumbnail:
  - `Extreme Ironing`
  - `Parodied Mona Lisa`
- Chúng biến thành hai chấm dữ liệu trên một trục:
  `qualitative examples -> quantitative benchmarks`
- Màn hình sau đó mở ra bảng benchmark.

### Content
Hai ví dụ cho trực giác: LLaVA phản hồi sâu, theo instruction, có reasoning. Nhưng để biết model mạnh đến đâu, cần nhìn benchmark rộng hơn.

### Narration Notes
"Demo giúp ta cảm được năng lực. Benchmark giúp ta đo năng lực đó trên nhiều dạng bài khác nhau."

### Technical Notes
- Dùng `ReplacementTransform` từ thumbnails sang các benchmark cards.
- Scene này ngắn, đóng vai trò transition.

---

## Scene 6: Benchmark Table - LLaVA-1.6-34B
**Duration**: ~90 giây
**Purpose**: Trình bày bảng benchmark được cung cấp, nhấn mạnh LLaVA-1.6-34B.

### Visual Elements
- Dựng lại bảng bằng shape/text:

| Model | MMMU (val) | MMMU (test) | MathVista | MMBench-EN | MMBench-CN | MM-Vet |
|---|---:|---:|---:|---:|---:|---:|
| GPT-4V | 56.8 | 55.7 | 49.9 | 75.8 | 73.9 | 67.6 |
| Gemini Ultra | 59.4 | - | 53 | - | - | - |
| Gemini Pro | 47.9 | - | 45.2 | 73.6 | 74.3 | 64.3 |
| LLaVA-1.5-13B | 36.4 | 33.6 | 27.6 | 67.8 | 63.3 | 36.3 |
| LLaVA-1.6-34B | 51.1 | 45.3 | 46.5 | 79.3 | 79 | 57.4 |

- Header màu navy.
- Hàng `LLaVA-1.6-34B` màu cam nhạt.
- Các ô LLaVA-1.6-34B thắng Gemini Pro được highlight:
  - `MMMU (val): 51.1 > 47.9`
  - `MMMU (test): 45.3`
  - `MathVista: 46.5 > 45.2`
  - `MMBench-EN: 79.3 > 73.6`
  - `MMBench-CN: 79 > 74.3`
- Riêng `MM-Vet`: ghi chú trung thực:
  `Gemini Pro vẫn cao hơn: 64.3 vs 57.4`

### Content
Bảng cho thấy LLaVA-1.6-34B cải thiện mạnh so với LLaVA-1.5-13B, đặc biệt ở MMMU, MathVista và MMBench. Nhưng nó không thắng mọi benchmark: MM-Vet vẫn là điểm Gemini Pro tốt hơn.

### Narration Notes
"Điều đáng nói không phải là LLaVA thắng tuyệt đối. Điều đáng nói là một open-source VLM đã bước vào cùng mặt bằng benchmark với các model rất mạnh."

### Technical Notes
- Không dùng screenshot trực tiếp; tái tạo bảng để animate được.
- Animate:
  1. Header xuất hiện.
  2. Các model proprietary hiện trước.
  3. LLaVA-1.5 hiện như baseline.
  4. LLaVA-1.6-34B trượt vào và sáng lên.
  5. Các ô thắng Gemini Pro được khoanh/circumscribe lần lượt.

---

## Scene 7: Radar Chart - LLaVA-1.5 Trên Nhiều Benchmark
**Duration**: ~110 giây
**Purpose**: Tái tạo radar chart bằng animation, cho thấy LLaVA-1.5 vượt các baseline trên nhiều trục.

### Visual Elements
- Radar chart có 12 trục:
  1. `VQAv2`
  2. `GQA`
  3. `VizWiz`
  4. `SQA-IMG`
  5. `TextVQA`
  6. `POPE`
  7. `MME`
  8. `MMBench`
  9. `MMBench-CN`
  10. `SEED-Bench`
  11. `LLaVA-Bench`
  12. `MM-Vet`
- 4 polygon lines:
  - BLIP-2: blue
  - InstructBLIP: green
  - Qwen-VL-Chat: orange
  - LLaVA-1.5: red
- LLaVA-1.5 polygon có fill đỏ nhạt.
- Legend ở góc phải dưới.

### Content
Radar chart thể hiện LLaVA-1.5 mạnh hơn trên nhiều benchmark visual understanding. Các giá trị quan trọng cho LLaVA-1.5:
- VQAv2 `80.0`
- GQA `63.3`
- VizWiz `53.6`
- SQA-IMG `71.6`
- TextVQA `61.3`
- POPE `85.9`
- MME `1531.3`
- MMBench `67.7`
- MMBench-CN `63.6`
- SEED-Bench `61.6`
- LLaVA-Bench `70.7`
- MM-Vet `35.4`

Baseline theo hình:
- Qwen-VL-Chat có nhiều điểm mạnh, ví dụ VQAv2 `78.2`, GQA `57.5`, SQA-IMG `68.2`, TextVQA `61.3`, MME `1487.5`, MMBench `60.6`, MMBench-CN `56.7`, SEED-Bench `58.2`.
- InstructBLIP nổi bật ở GQA `49.5`, TextVQA `50.7`, SEED-Bench `53.4`, nhưng thấp hơn LLaVA-1.5 ở nhiều trục.
- BLIP-2 thấp hơn rõ ở phần lớn trục, ví dụ MME `1293.8`.

### Narration Notes
"Radar chart này cho ta một cảm giác hình học: model nào phủ được diện tích rộng hơn thì có năng lực cân bằng hơn trên nhiều dạng bài. Đường đỏ của LLaVA-1.5 mở rộng ra ở nhiều trục, không chỉ một benchmark đơn lẻ."

### Technical Notes
- Không dùng ảnh radar chart screenshot. Hãy vẽ lại bằng Manim.
- Cách dựng:
  1. Tạo 12 vector hướng cách đều nhau quanh tâm.
  2. Vẽ các vòng tròn hoặc polygon grid mờ.
  3. Gắn label benchmark quanh ngoài.
  4. Chuẩn hóa từng benchmark về radius riêng để dễ nhìn. Với MME scale lớn, normalize theo max của MME; với các benchmark phần trăm, normalize theo 100.
  5. Tạo polygon cho từng model bằng `Polygon(*points)`.
  6. Animate lần lượt:
     - grid xuất hiện.
     - BLIP-2 polygon vẽ trước.
     - InstructBLIP.
     - Qwen-VL-Chat.
     - LLaVA-1.5 cuối cùng, line đỏ dày hơn và fill nhạt.
- Có thể dùng `Create(polyline)` và `FadeIn(fill_polygon)`.
- Các số trên trục chỉ nên hiện cho LLaVA-1.5 hoặc vài điểm chính để tránh rối.

---

## Scene 8: Kết Luận - LLaVA Mạnh Ở Đâu?
**Duration**: ~60 giây
**Purpose**: Chốt thông điệp chính của scene.

### Visual Elements
- Ba cột recap:
  1. `Detailed Response`
     - hiểu ảnh và giải thích kĩ.
  2. `Visual Reasoning`
     - phát hiện unusual / unsafe / parody.
  3. `Benchmark Strength`
     - thể hiện qua bảng và radar chart.
- Ảnh `Yellow.png` thu nhỏ bay vào cột 1-2.
- Ảnh Mona Lisa bay vào cột 2.
- Radar chart thu nhỏ bay vào cột 3.
- Dòng cuối:
  `LLaVA = nhìn ảnh + hiểu instruction + suy luận bằng ngôn ngữ`

### Content
Kết luận rằng LLaVA mạnh ở khả năng kết nối nhận thức thị giác với instruction-following của LLM. Nó không chỉ gọi tên object, mà còn giải thích tình huống và đưa ra câu trả lời có cấu trúc.

### Narration Notes
"Từ ví dụ chiếc xe vàng đến Mona Lisa parody, rồi sang benchmark, cùng một ý tưởng lặp lại: LLaVA dùng ảnh như một phần của cuộc hội thoại, không chỉ như một ảnh để caption."

### Technical Notes
- Dùng `ReplacementTransform` từ các visual trước về ba cột recap.
- Dòng cuối có thể dùng `Text`, không cần `MathTex`.

---

## Transitions & Flow
- Scene 1 -> 2: Câu hỏi chung tách thành 4 response cards.
- Scene 2 -> 3: LLaVA response được phân rã thành 4 lớp reasoning.
- Scene 3 -> 4: Từ `unusual scene` chuyển sang `cultural reference`.
- Scene 4 -> 5: Hai ví dụ co lại thành qualitative examples.
- Scene 5 -> 6: Qualitative examples biến thành benchmark table.
- Scene 6 -> 7: Bảng benchmark xoay thành radar chart để thể hiện nhiều chiều năng lực.
- Scene 7 -> 8: Radar chart thu nhỏ, nhập vào recap.

## Recurring Visual Motifs
- **Blue**: visual perception, ảnh, object/action.
- **Green**: LLaVA answer, language understanding.
- **Yellow**: instruction/question, điểm cần chú ý.
- **Orange**: improvement / LLaVA-1.6.
- **Red**: highlight điều unusual hoặc lỗi/thiếu chính xác của baseline.
- **Response cards**: mỗi model là một card riêng để so sánh dễ.
- **Radar line đỏ**: LLaVA-1.5 là đường cuối cùng và nổi bật nhất.

## Color Palette
- Visual Blue `#58C4DD`
- Language Green `#83C167`
- Connector Yellow `#FFFF00`
- Improvement Orange `#FF8C2A`
- Warning Red `#FF6666`
- Background Dark Gray `#1C1C1C`
- Table Header Navy `#1D3F6E`
- Table Highlight Peach `#F7D9C8`

## Quantitative Content

### Benchmark Table
| Model | MMMU (val) | MMMU (test) | MathVista | MMBench-EN | MMBench-CN | MM-Vet |
|---|---:|---:|---:|---:|---:|---:|
| GPT-4V | 56.8 | 55.7 | 49.9 | 75.8 | 73.9 | 67.6 |
| Gemini Ultra | 59.4 | - | 53 | - | - | - |
| Gemini Pro | 47.9 | - | 45.2 | 73.6 | 74.3 | 64.3 |
| LLaVA-1.5-13B | 36.4 | 33.6 | 27.6 | 67.8 | 63.3 | 36.3 |
| LLaVA-1.6-34B | 51.1 | 45.3 | 46.5 | 79.3 | 79 | 57.4 |

### Radar Chart Axes
- `VQAv2`, `GQA`, `VizWiz`, `SQA-IMG`, `TextVQA`, `POPE`, `MME`, `MMBench`, `MMBench-CN`, `SEED-Bench`, `LLaVA-Bench`, `MM-Vet`

### LLaVA-1.5 Radar Values
- VQAv2 `80.0`
- GQA `63.3`
- VizWiz `53.6`
- SQA-IMG `71.6`
- TextVQA `61.3`
- POPE `85.9`
- MME `1531.3`
- MMBench `67.7`
- MMBench-CN `63.6`
- SEED-Bench `61.6`
- LLaVA-Bench `70.7`
- MM-Vet `35.4`

## Asset Notes
- Main yellow image: `image/scene4/Yellow.png`
- Repo path currently likely available: `media/images/Scene4_vi/Yellow.png`
- Mona Lisa parody image: use saved image in `image/scene4` or current repo path `media/images/Scene4_vi/Monalisa.png`
- Radar chart screenshot is reference only. The animation should recreate the chart using shapes.
- Benchmark table screenshot is reference only. The animation should recreate the table using shapes/text.

## Implementation Order
1. Scene 1: load `Yellow.png`, show question.
2. Scene 2: build response cards and comparison.
3. Scene 3: decompose LLaVA response into reasoning layers.
4. Scene 4: Mona Lisa parody and cultural reference reasoning.
5. Scene 6: benchmark table, because it is mostly static and useful for style.
6. Scene 7: radar chart animation, most complex part.
7. Scene 5 and Scene 8: transitions/recap after core visuals are stable.
