[English](architecture.en.md) | [繁體中文](architecture.zh-TW.md)

# 系統架構與資料流

範例中的 Donor 是五個 IAB Node 的上游站台。
每個 Node 在邏輯上關聯一個 UE，並讀取分配給它的 Tag。
Tag 部署在所屬 Node 周圍；模擬期間拓撲保持固定。

1. **拓撲：** Node 位置、Tag 數量與亂數種子產生拓撲快照、表格與部署圖。快照記錄 Node、Tag 與其關係。
2. **通道：** 拓撲快照、通道設定與窗功率作為輸入，用於計算接收功率、SNR、SINR 與封包接收結果。SNR 比較訊號與噪聲功率；SINR 也考慮干擾。
3. **結果：** Notebook 顯示設定與計算過程。拓撲模組也能將圖與資料匯出為 PNG、SVG、JSON 和 CSV。

拓撲的近、中、遠區表示距離，不能證明 RF 覆蓋範圍、沒有干擾或實測訊號品質。

通道模型採用研究假設，並假設封包已具備傳送條件；其結果不能保證戶外場域性能。
[通道指南](../ReferDoc/Implementation/ChannelModel/README.md)說明模型假設與參數來源。
IAB split 架構中的 Tag 讀取屬於研究擴充，並非完整符合標準的宣稱。

## 模組單元與延伸閱讀

- [拓撲單元](unit/iab-topology.zh-TW.md)
- [通道模型單元](unit/channel-model.zh-TW.md)

核心程式分為處理拓撲的 [src/iab](../src/iab/) 與計算通道的 [src/channel](../src/channel/)。對應測試位於 [tests/iab](../tests/iab/) 與 [tests/channel](../tests/channel/)。

- [整體架構](../docs/architecture/system.html)
- [IAB 拓撲架構](../docs/architecture/iab-topology.html)與[設計說明](../docs/architecture/iab-topology-design.md)
- [通道架構](../docs/architecture/channel-model.html)

