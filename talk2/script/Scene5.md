# Scene 5: ViP-LLaVA - LLaVA Hiểu Các Chỉ Thị Hình Ảnh

## Overview
- **Topic**: ViP-LLaVA mở rộng LLaVA để hiểu `visual prompts`: mũi tên, nét vẽ, điểm chấm, mask, bounding box và các ký hiệu vẽ trực tiếp trên ảnh.
- **Hook**: Nếu người dùng không muốn nói "đối tượng ở tọa độ `[x_1, y_1, x_2, y_2]`", mà chỉ muốn vẽ một mũi tên vào ảnh thì model có hiểu không?
- **Target Audience**: Người học đã biết LLaVA/VLM ở mức cơ bản, chưa cần biết chi tiết training.
- **Estimated Length**: ~5-6 phút.
- **Key Insight**: ViP-LLaVA biến một thao tác rất tự nhiên của con người thành input cho model: vẽ thẳng lên ảnh, trộn nó với ảnh gốc bằng `Alpha Blending`, rồi để visual encoder và LLM cùng suy luận.

## Asset Notes
- Thư mục user nói: `Talk2/Image/Scene5`.
- Thư mục hiện có trong repo: `Talk2/Image/Sccene5`.
- Asset kiến trúc: `Talk2/Image/Sccene5/ViP-LLaVA_Architecture.png`.
- Asset 8 prompt types:
  - `Talk2/Image/Sccene5/Mask contour.png`
  - `Talk2/Image/Sccene5/Ellipse.png`
  - `Talk2/Image/Sccene5/Bounding Box.png`
  - `Talk2/Image/Sccene5/Triangle.png`
  - `Talk2/Image/Sccene5/Scribble.png`
  - `Talk2/Image/Sccene5/Point.png`
  - `Talk2/Image/Sccene5/Arrow.png`
  - `Talk2/Image/Sccene5/Mask.png`

## Narrative Arc
Video bắt đầu từ một giới hạn rất thực tế: các LMM trước đây hiểu toàn bộ ảnh khá tốt, nhưng lúng túng khi người dùng muốn hỏi về đúng một vùng cụ thể. Thay vì bắt người dùng nhập tọa độ hoặc token vị trí, ViP-LLaVA đưa ra một ý tưởng gần như quá đơn giản: cứ vẽ dấu hiệu trực quan lên ảnh, trộn ảnh lại, rồi đưa vào pipeline của LLaVA. Sau đó, video mở rộng thành 8 kiểu `visual prompt` mà model có thể hiểu.

---

## Scene 1: Không Chỉ Hỏi Về Cả Bức Ảnh
**Duration**: ~45 giây  
**Purpose**: Đặt vấn đề: LLaVA hiểu ảnh tổng thể, nhưng interaction tự nhiên cần hỏi về vùng cụ thể.

### Visual Elements
- Một ảnh minh họa chung ở trung tâm, bên trên có title:
  `LLaVA hiểu ảnh. Nhưng hiểu "vùng tôi đang chỉ" thì sao?`
- Overlay một câu hỏi chung:
  `What is happening in this image?`
- Sau đó xuất hiện câu hỏi cụ thể hơn:
  `What is the person marked by this arrow doing?`
- Mũi tên vàng hoặc scribble vẽ trực tiếp lên một vùng ảnh.

### Content
Mở đầu bằng sự khác nhau giữa `image-level understanding` và `region-level instruction following`. Nếu câu hỏi chỉ nói về toàn bộ ảnh, LMM có thể trả lời khá ổn. Nhưng khi người dùng muốn hỏi về "người này", "vật được khoanh này", hoặc "vùng tôi gạch ở đây", model cần hiểu chỉ thị hình ảnh chứ không chỉ hiểu text.

### Narration Notes
"Con người không giao tiếp với ảnh bằng tọa độ. Ta chỉ tay, vẽ mũi tên, khoanh tròn, hoặc gạch một nét lên vùng cần chú ý. Câu hỏi là: một model như LLaVA có thể hiểu kiểu chỉ thị tự nhiên đó không?"

### Technical Notes
- Dùng `ImageMobject` cho ảnh nền.
- Dùng `Arrow`, `Circle`, hoặc `VMobject` scribble để mô phỏng prompt vẽ tay.
- Dùng `Transform` từ câu hỏi tổng quát sang câu hỏi theo vùng.

---

## Scene 2: Hạn Chế Của Prior / Concurrent Work
**Duration**: ~65 giây  
**Purpose**: Giải thích vì sao cách cũ chưa tự nhiên với người dùng.

### Visual Elements
- Màn hình chia hai bên:
  - Trái: `Natural human prompt`
    - Một mũi tên / scribble vẽ trên ảnh.
    - Text: `Chỉ vào đây`
  - Phải: `Prior region methods`
    - Text box chứa dạng nhập tọa độ:
      `[x_1, y_1, x_2, y_2]`
    - Ví dụ:
      `text (A) within <bbox>`
      `region token`
      `learned position embedding`
- Tên model xuất hiện thành một hàng nhỏ:
  `Shikra`, `MiniGPT-v2`, `Ferret`, `GPT4ROI`, `Kosmos-2`

### Content
Các mô hình trước đó có thể làm `region understanding`, nhưng thường cần input dạng text có cấu trúc, bounding box, region token, hoặc embedding vị trí được học trước. Điều này làm interaction trở nên ít tự nhiên: người dùng phải diễn đạt vị trí bằng một format máy móc thay vì vẽ thẳng lên ảnh.

### Narration Notes
"Điểm yếu không phải là các model này không biết vùng ảnh. Điểm yếu là cách nói chuyện với chúng chưa giống cách con người thật sự chỉ vào ảnh."

### Technical Notes
- Dùng các card mỏng, không quá nhiều chữ.
- Animate tọa độ `[x_1, y_1, x_2, y_2]` rơi vào một hộp "machine format".
- Dùng `Cross` nhẹ hoặc fade màu xám cho phần "không tự nhiên".

---

## Scene 3: Ý Tưởng Của ViP-LLaVA - Super Simple
**Duration**: ~75 giây  
**Purpose**: Trình bày trực giác cốt lõi: vẽ prompt lên ảnh rồi đưa ảnh đã trộn vào model.

### Visual Elements
- Bên trái: `Original Image`
- Ở giữa: `Visual Prompt`
  - arrow / scribble / mask dạng màu vàng.
- Dấu cộng giữa hai lớp:
  `Image + Visual Prompt`
- Bên phải: `Prompted Image`
  - ảnh đã được overlay.
- Công thức LaTeX ở dưới:
  `\tilde{X}_v = \alpha P_v + (1 - \alpha) X_v`
- Các nhãn quan trọng:
  - `Alpha Blending`
  - `freeform visual prompts`
  - `no coordinate typing`

### Content
ViP-LLaVA không tạo một module region encoding phức tạp. Nó trực tiếp overlay dấu hiệu trực quan lên ảnh RGB, tạo ra ảnh mới đã chứa ý định của người dùng. Sau đó ảnh này đi qua pipeline gần giống LLaVA.

### Narration Notes
"Đây là phần đẹp nhất: thay vì dạy model một ngôn ngữ tọa độ mới, ta đưa chỉ thị vào đúng nơi nó thuộc về: trong ảnh."

### Technical Notes
- Công thức dùng `MathTex(r"\tilde{X}_v = \alpha P_v + (1-\alpha)X_v")`.
- Dùng `ReplacementTransform` từ `Original Image` + `Visual Prompt` sang `Prompted Image`.
- Màu:
  - ảnh gốc: xanh dương nhạt.
  - visual prompt: vàng.
  - ảnh blended: xanh lá.

---

## Scene 4: Pipeline Kiến Trúc ViP-LLaVA
**Duration**: ~70 giây  
**Purpose**: Cho thấy luồng xử lý đầy đủ từ ảnh đã blended và câu hỏi text tới câu trả lời.

### Visual Elements
- Dùng asset `Talk2/Image/Sccene5/ViP-LLaVA_Architecture.png` đặt lớn ở giữa.
- Highlight theo từng đoạn:
  1. `Alpha Blended Image`
  2. `CLIP Image Encoder`
  3. `Fusion & LN & MLP`
  4. `LLM`
  5. `Answer`
- Một text prompt chạy song song phía dưới:
  `What is the person marked by the scribble trying to do?`

### Content
Bức ảnh đã được vẽ đè đi qua `CLIP Image Encoder`. Visual features tiếp tục qua các lớp kết nối như `Fusion`, `LayerNorm`, và `MLP` để chuyển thành dạng LLM dùng được. Song song với đó, câu hỏi text của người dùng cũng được nhúng rồi đưa vào LLM. LLM nhận cả visual context lẫn language instruction để sinh câu trả lời.

### Narration Notes
"Visual prompt không đứng ngoài pipeline. Nó được hòa vào ảnh ngay từ đầu, vì vậy image encoder có thể nhìn thấy cả nội dung ảnh lẫn dấu hiệu mà người dùng vẽ."

### Technical Notes
- Nếu asset kiến trúc có chữ nhỏ, phóng to và pan camera nhẹ qua từng vùng.
- Dùng `SurroundingRectangle` hoặc `RoundedRectangle` mỏng để highlight từng module.
- Không cần vẽ lại toàn bộ kiến trúc nếu ảnh đã rõ; chỉ animate các nhãn và vùng highlight.

---

## Scene 5: Tại Sao Alpha Blending Lại Hợp Lý?
**Duration**: ~55 giây  
**Purpose**: Làm rõ vì sao một kỹ thuật đơn giản vẫn hiệu quả.

### Visual Elements
- Ba lớp chồng lên nhau theo chiều dọc:
  1. `RGB image`
  2. `Prompt layer`
  3. `Blended input`
- Một slider `\alpha` chạy từ 0 tới 1.
- Khi `\alpha` tăng, prompt hiện rõ hơn.
- Dòng insight:
  `Ý định của người dùng trở thành một phần của input visual.`

### Content
Alpha blending kiểm soát mức độ prompt phủ lên ảnh. Nếu prompt quá mờ, model khó thấy dấu hiệu. Nếu quá đậm, prompt che mất nội dung ảnh. ViP-LLaVA dùng cách hòa trộn này để giữ cả hai: ảnh gốc và chỉ thị của người dùng.

### Narration Notes
"Cái hay là prompt không thay thế ảnh. Nó chỉ thêm một lớp tín hiệu: đủ rõ để model chú ý, nhưng vẫn giữ ngữ cảnh thị giác xung quanh."

### Technical Notes
- Có thể dùng `ValueTracker` cho `alpha`.
- Nếu code nhanh, chỉ cần dùng 3 frame ảnh minh họa thay vì blending thật.
- Công thức giữ cố định ở góc:
  `\tilde{X}_v = \alpha P_v + (1-\alpha)X_v`

---

## Scene 6: Tám Kiểu Visual Prompt
**Duration**: ~85 giây  
**Purpose**: Giới thiệu đủ 8 loại ký hiệu mà ViP-LLaVA hỗ trợ.

### Visual Elements
- Grid 4x2 gồm 8 ảnh:
  1. `Mask contour` - `Talk2/Image/Sccene5/Mask contour.png`
  2. `Ellipse` - `Talk2/Image/Sccene5/Ellipse.png`
  3. `Bounding box` - `Talk2/Image/Sccene5/Bounding Box.png`
  4. `Triangle` - `Talk2/Image/Sccene5/Triangle.png`
  5. `Scribble` - `Talk2/Image/Sccene5/Scribble.png`
  6. `Point` - `Talk2/Image/Sccene5/Point.png`
  7. `Arrow` - `Talk2/Image/Sccene5/Arrow.png`
  8. `Mask` - `Talk2/Image/Sccene5/Mask.png`
- Mỗi ảnh có label song ngữ:
  - `Mask contour / Viền mặt nạ`
  - `Ellipse / Hình elip`
  - `Bounding box / Hộp giới hạn`
  - `Triangle / Hình tam giác`
  - `Scribble / Nét vẽ nguệch ngoạc`
  - `Point / Điểm chấm`
  - `Arrow / Mũi tên`
  - `Mask / Mặt nạ phủ kín`

### Content
ViP-LLaVA không chỉ hiểu một kiểu đánh dấu cố định. Nó được huấn luyện với nhiều hình dạng, màu sắc, độ trong suốt, độ dày nét, kích thước và hướng khác nhau. Điều này giúp model hiểu các `freeform visual prompts` gần với hành vi thật của người dùng.

### Narration Notes
"Có người thích khoanh vùng. Có người chấm một điểm. Có người vẽ mũi tên. Có người chỉ gạch một nét nguệch ngoạc. ViP-LLaVA cố gắng biến tất cả những cách chỉ này thành một ngôn ngữ thị giác chung."

### Technical Notes
- Dùng `Group` hoặc `VGroup` cho từng tile: `image_card + label`.
- Nên animate theo cặp:
  - contour + mask
  - ellipse + bounding box
  - point + arrow
  - triangle + scribble
- Dùng màu label khác nhau nhưng nền vẫn tối kiểu 3b1b.

---

## Scene 7: Một Câu Hỏi, Một Vùng Được Đánh Dấu
**Duration**: ~60 giây  
**Purpose**: Minh họa cách model trả lời câu hỏi phụ thuộc vào vùng được prompt.

### Visual Elements
- Một ảnh có nhiều đối tượng/người.
- Lần 1: dùng `Arrow` chỉ vào object A.
- Câu hỏi:
  `What is the marked person trying to do?`
- Câu trả lời xuất hiện.
- Lần 2: prompt chuyển sang object B bằng `ReplacementTransform`.
- Câu trả lời thay đổi.
- Dòng kết luận:
  `Same image, different visual prompt -> different answer`

### Content
Cùng một bức ảnh có thể chứa nhiều đối tượng. Nếu chỉ hỏi bằng text, câu hỏi có thể mơ hồ. Visual prompt làm cho instruction trở nên cụ thể về không gian: model biết cần tập trung vào vùng nào.

### Narration Notes
"Điểm quan trọng là visual prompt không chỉ trang trí. Nó thay đổi câu hỏi. Cùng một ảnh, cùng một câu chữ, nhưng prompt khác nhau thì đáp án phải khác nhau."

### Technical Notes
- Có thể dùng một trong các ảnh prompt type làm ví dụ nếu chưa có ảnh riêng.
- Dùng `Transform` prompt A sang prompt B, rồi `TransformMatchingShapes` cho answer card.
- Dùng màu vàng cho prompt để nhất quán với scene alpha blending.

---

## Scene 8: Dữ Liệu Huấn Luyện - Từ Annotation Thành Prompt Tự Nhiên
**Duration**: ~55 giây  
**Purpose**: Tóm tắt cách ViP-LLaVA tận dụng dữ liệu có sẵn để sinh visual prompts.

### Visual Elements
- Luồng 3 bước:
  1. `Existing annotations`
     - bounding box / segmentation mask.
  2. `Generate visual prompts`
     - box, ellipse, arrow, scribble, mask...
  3. `Region-level instruction data`
     - image + visual prompt + question + answer.
- Một nhãn nhỏ:
  `Dựa trên visual prompt annotations từ Shtedritski et al., ICCV 2023`

### Content
ViP-LLaVA tận dụng một phần dữ liệu tiền huấn luyện/annotation có sẵn liên quan đến CLIP và visual prompt. Từ bounding box hoặc mask, hệ thống có thể tạo nhiều dạng prompt trực quan khác nhau để huấn luyện model hiểu cách con người đánh dấu vùng quan tâm.

### Narration Notes
"Ta không cần viết tay mọi ví dụ. Từ annotation có sẵn, có thể sinh ra nhiều kiểu chỉ thị thị giác khác nhau, rồi dạy model: khi thấy dấu này, hãy hiểu vùng này là trọng tâm."

### Technical Notes
- Dùng `Arrow` nối 3 card.
- Dùng icon nhỏ hoặc shape minh họa annotation.
- Giữ scene gọn, tránh đi quá sâu vào dataset.

---

## Scene 9: Aha Moment - Visual Prompt Là Ngôn Ngữ Không Gian
**Duration**: ~45 giây  
**Purpose**: Kết lại bằng insight chính, không biến thành benchmark scene.

### Visual Elements
- Bên trái: `Text prompt`
  - `Describe the object in the red box.`
- Bên phải: `Visual prompt`
  - ảnh có mũi tên/scribble.
- Hai luồng nhập vào cùng một LLM icon.
- Câu chốt lớn:
  `Visual prompts = spatial instructions`
- Dòng phụ:
  `Tự nhiên hơn tọa độ. Cụ thể hơn caption toàn ảnh.`

### Content
ViP-LLaVA mở rộng cách con người nói chuyện với multimodal models. Ta không chỉ gõ câu hỏi, mà còn có thể dùng thao tác thị giác để chỉ định vùng cần suy luận.

### Narration Notes
"Sau LLaVA, model có thể nhìn ảnh và trò chuyện. Với ViP-LLaVA, ta tiến thêm một bước: người dùng có thể chỉ vào ảnh theo cách rất con người, và model hiểu được ý định không gian đó."

### Technical Notes
- Kết bằng `FadeTransform` 8 prompt types thành một cụm `spatial instructions`.
- Dùng `Circumscribe` cho câu chốt.

---

## Transitions & Flow
- Motif chính: một nét vẽ vàng đi xuyên suốt video.
- Từ Scene 1 sang Scene 2: mũi tên người dùng vẽ biến thành bounding box tọa độ, tạo cảm giác "tự nhiên bị máy móc hóa".
- Từ Scene 2 sang Scene 3: bounding box text tan ra, trở lại thành visual prompt trên ảnh.
- Từ Scene 3 sang Scene 4: ảnh blended bay vào kiến trúc ViP-LLaVA.
- Từ Scene 5 sang Scene 6: slider alpha dừng lại, prompt layer tách thành 8 kiểu prompt.
- Từ Scene 8 sang Scene 9: annotation/training pipeline thu gọn thành insight cuối.

## Color Palette
- **Background**: `#1C1C1C` - nền tối kiểu 3b1b.
- **Visual prompt accent**: `#FFFF00` - mũi tên, scribble, alpha layer.
- **Vision path**: `#58C4DD` - ảnh, CLIP Image Encoder.
- **Language path**: `#83C167` - text question, LLM answer.
- **Region / warning**: `#FF6666` - hạn chế của phương pháp cũ.
- **Architecture / bridge**: `#FF8C2A` - Fusion, LN, MLP.

## Mathematical / Technical Content
- Công thức alpha blending:
  ```latex
  \tilde{X}_v = \alpha P_v + (1-\alpha)X_v
  ```
- Trong đó:
  - `X_v`: ảnh gốc.
  - `P_v`: visual prompt layer.
  - `\alpha`: độ trong suốt của prompt.
  - `\tilde{X}_v`: ảnh đã được prompt/blended.
- Thuật ngữ giữ English:
  `Visual Prompt`, `Alpha Blending`, `CLIP Image Encoder`, `Fusion`, `LayerNorm`, `MLP`, `LLM`, `freeform visual prompts`, `region-level instruction`.

## Implementation Order
1. Tạo helper `image_card`, `text_card`, `prompt_overlay`, `section_title`.
2. Code Scene 3 trước vì nó chứa motif alpha blending cốt lõi.
3. Code Scene 6 sau vì cần kiểm tra đủ 8 asset prompt types.
4. Code Scene 4 bằng ảnh kiến trúc có sẵn và các highlight rectangle.
5. Code các scene còn lại bằng card/arrow/transform dựa trên helper đã có.
6. Render thử từng scene bằng `manim -ql -s` để kiểm tra chữ tiếng Việt, nhất là label song ngữ.

## References
- ViP-LLaVA project page: https://vip-llava.github.io/
- CVPR 2024 paper: https://openaccess.thecvf.com/content/CVPR2024/papers/Cai_ViP-LLaVA_Making_Large_Multimodal_Models_Understand_Arbitrary_Visual_Prompts_CVPR_2024_paper.pdf
