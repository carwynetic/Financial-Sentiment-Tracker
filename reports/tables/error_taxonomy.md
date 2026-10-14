# Qualitative Failure Mode Analysis & Error Taxonomy (FinBERT Fine-Tuned)

- **Tổng số ca kiểm thử**: 518
- **Tổng số ca FinBERT đoán sai**: 41 (7.92%)
- **Độ chính xác toàn cục**: 92.08%

## 1. Thống kê phân bố các dạng lỗi nhầm lẫn

| Error Mode (True -> Pred) | Count | Percentage of Errors |
| :--- | :---: | :---: |
| `Neutral -> Positive` | 13 | 31.7% |
| `Positive -> Neutral` | 12 | 29.3% |
| `Positive -> Negative` | 8 | 19.5% |
| `Negative -> Positive` | 4 | 9.8% |
| `Neutral -> Negative` | 3 | 7.3% |
| `Negative -> Neutral` | 1 | 2.4% |

## 2. Phân tích chi tiết các mẫu câu lỗi tiêu biểu

### Dạng lỗi: `Neutral -> Positive`

- **Sentence**: *"The idea of saving electricity in data transfer is still a new one ."*
  - **Ground Truth**: `Neutral` | **FinBERT Prediction**: `Positive`
- **Sentence**: *"Following the issue , the number of shares in the Swedish company will grow by 9 % ."*
  - **Ground Truth**: `Neutral` | **FinBERT Prediction**: `Positive`
- **Sentence**: *"To raise consumer awareness and encourage people to recycle their old mobile devices Nokia runs regular recycling campaigns around the world ."*
  - **Ground Truth**: `Neutral` | **FinBERT Prediction**: `Positive`

### Dạng lỗi: `Positive -> Neutral`

- **Sentence**: *"According to Deputy MD Pekka Silvennoinen the aim is double turnover over the next three years ."*
  - **Ground Truth**: `Positive` | **FinBERT Prediction**: `Neutral`
- **Sentence**: *"For Telenor , the three and a half year contract is worth an estimated 12.6 m. YIT has chosen Telenor and Elisa as its principal suppliers of ICT solutions in Norway , Sweden , Denmark and Finland ."*
  - **Ground Truth**: `Positive` | **FinBERT Prediction**: `Neutral`
- **Sentence**: *"The original name Componenta +àm+Ñl , as a subsidiary of the Finnish Componenta Group , has been changed to +àm+Ñl Components and the company has seen a 63 % growth in Q1 2010 , in comparison to Q1 2009 ."*
  - **Ground Truth**: `Positive` | **FinBERT Prediction**: `Neutral`

### Dạng lỗi: `Positive -> Negative`

- **Sentence**: *"In the second quarter of 2010 , the group 's pretax loss narrowed to EUR 400,000 from EUR 600,000 ."*
  - **Ground Truth**: `Positive` | **FinBERT Prediction**: `Negative`
- **Sentence**: *"28 October 2010 - Finnish wood products technology supplier Raute Oyj HEL : RUTAV said today it swung to a net profit of EUR3m for the first nine months of 2010 versus a net loss of EUR5 .2 m for the same period a year earlier ."*
  - **Ground Truth**: `Positive` | **FinBERT Prediction**: `Negative`
- **Sentence**: *"ADP News - Nov 6 , 2008 - Finnish retail software developer Aldata Solution Oyj OMX : ALD1V said today that it swung to a net profit of EUR 2.1 million USD 2.7 m for the first nine months of 2008 versus a net loss of EU"*
  - **Ground Truth**: `Positive` | **FinBERT Prediction**: `Negative`

### Dạng lỗi: `Negative -> Positive`

- **Sentence**: *"Coca-Cola was the market leader of manufacturers with a market share of 36.9 % , down 2.2 % from the corresponding period in 2004-2005 ."*
  - **Ground Truth**: `Negative` | **FinBERT Prediction**: `Positive`
- **Sentence**: *"Finnish power supply solutions and systems provider Efore Oyj said its net loss widened to 3.2 mln euro $ 4.2 mln for the first quarter of fiscal 2006-2007 ending October 31 , 2007 from 900,000 euro $ 1.2 mln for the same period of fiscal 2005-06 ."*
  - **Ground Truth**: `Negative` | **FinBERT Prediction**: `Positive`
- **Sentence**: *"Currently , the company foresees its pre-tax profit to remain below the 2009 level when it reached EUR 700,000 USD 934,000 , compared with previous projections of a slightly better pre-tax profit ."*
  - **Ground Truth**: `Negative` | **FinBERT Prediction**: `Positive`

### Dạng lỗi: `Neutral -> Negative`

- **Sentence**: *"A huge issue for us is the button placement ."*
  - **Ground Truth**: `Neutral` | **FinBERT Prediction**: `Negative`
- **Sentence**: *"Another noticeable thing is that the search for Tata and Airtel brands was mostly related to ` broadband connections ' ."*
  - **Ground Truth**: `Neutral` | **FinBERT Prediction**: `Negative`
- **Sentence**: *"As a consequence the Works Council had withdrawn its petition to suspend the reorganisation ."*
  - **Ground Truth**: `Neutral` | **FinBERT Prediction**: `Negative`

### Dạng lỗi: `Negative -> Neutral`

- **Sentence**: *"The contracts of the employees , 96 of whom are blue-collar workers , will be ended between March and August 2011 ."*
  - **Ground Truth**: `Negative` | **FinBERT Prediction**: `Neutral`

