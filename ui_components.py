import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF, QPropertyAnimation, Property, QEasingCurve, QObject
from PySide6.QtGui import QPainter, QPolygonF, QColor, QPen, QBrush, QFont

class RadarChartWidget(QWidget):
    """
    Animasyonlu ve profesyonel Radar Grafik bileşeni.
    Veri değişimlerinde pürüzsüz geçişler sağlar.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(260, 260) # Boyutu sabitleyip dengelemek daha güvenli
        
        # Animasyon için saklanan değerler
        self._v1 = 0.0
        self._v2 = 0.0
        self._v3 = 0.0
        self._v4 = 0.0
        self._v5 = 0.0
        
        self.labels = ["Length", "Variety", "Entropy", "Uniques", "Safety"]
        
        # Tema Renkleri (Varsayılan Dark)
        self.grid_color = QColor("#334155")
        self.label_color = QColor("#94a3b8")

    def set_theme(self, is_dark):
        """Tema renklerini günceller."""
        if is_dark:
            self.grid_color = QColor("#334155")
            self.label_color = QColor("#94a3b8")
        else:
            self.grid_color = QColor("#cbd5e1")
            self.label_color = QColor("#475569")
        self.update()

    # Animasyon için Property tanımları
    def get_v1(self): return self._v1
    def set_v1(self, v): self._v1 = v; self.update()
    v1 = Property(float, get_v1, set_v1)

    def get_v2(self): return self._v2
    def set_v2(self, v): self._v2 = v; self.update()
    v2 = Property(float, get_v2, set_v2)

    def get_v3(self): return self._v3
    def set_v3(self, v): self._v3 = v; self.update()
    v3 = Property(float, get_v3, set_v3)

    def get_v4(self): return self._v4
    def set_v4(self, v): self._v4 = v; self.update()
    v4 = Property(float, get_v4, set_v4)

    def get_v5(self): return self._v5
    def set_v5(self, v): self._v5 = v; self.update()
    v5 = Property(float, get_v5, set_v5)

    def animate_to(self, metrics):
        """Tüm değerleri aynı anda hedef metriklere taşıyan animasyonu başlatır."""
        duration = 400
        targets = [
            metrics.get("length", 0),
            metrics.get("variety", 0),
            metrics.get("entropy", 0),
            metrics.get("uniqueness", 0),
            metrics.get("safety", 0)
        ]
        
        props = [b"v1", b"v2", b"v3", b"v4", b"v5"]
        
        for i, target in enumerate(targets):
            anim = QPropertyAnimation(self, props[i])
            anim.setDuration(duration)
            anim.setEndValue(float(target))
            anim.setEasingCurve(QEasingCurve.OutQuad)
            anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.contentsRect()
        center = rect.center()
        radius = 80 # Grafik alanı yarıçapı
        
        # 1. Arkaplan Ağını Çiz
        self._draw_grid(painter, center, radius)
        
        # 2. Veri Poligonunu Çiz
        self._draw_data_polygon(painter, center, radius)
        
        # 3. Etiketleri Çiz
        self._draw_labels(painter, center, radius)

    def _draw_grid(self, painter, center, radius):
        pen = QPen(self.grid_color, 1)
        painter.setPen(pen)
        
        for i in range(1, 5):
            r = radius * (i / 4)
            poly = self._get_poly(center, r)
            painter.drawPolygon(poly)
            
        # Eksen çizgileri
        outer_poly = self._get_poly(center, radius)
        painter.setPen(QPen(QColor("#334155"), 1, Qt.DotLine))
        for i in range(5):
            painter.drawLine(center, outer_poly[i])

    def _draw_data_polygon(self, painter, center, radius):
        values = [self._v1, self._v2, self._v3, self._v4, self._v5]
        if not any(values): return
        
        poly = QPolygonF()
        for i, v in enumerate(values):
            angle = math.radians(i * 72 - 90)
            p = QPointF(
                center.x() + radius * v * math.cos(angle),
                center.y() + radius * v * math.sin(angle)
            )
            poly.append(p)
            
        color = QColor("#38bdf8")
        painter.setPen(QPen(color, 2))
        fill_color = QColor(color)
        fill_color.setAlpha(80)
        painter.setBrush(QBrush(fill_color))
        painter.drawPolygon(poly)

    def _draw_labels(self, painter, center, radius):
        painter.setPen(self.label_color)
        painter.setFont(QFont("Inter", 8, QFont.Bold))
        
        for i, text in enumerate(self.labels):
            angle = math.radians(i * 72 - 90)
            dist = radius + 25
            x = center.x() + dist * math.cos(angle)
            y = center.y() + dist * math.sin(angle)
            
            # Etiket metnini ortala
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text)
            th = fm.height()
            painter.drawText(x - tw/2, y + th/4, text)

    def _get_poly(self, center, radius):
        poly = QPolygonF()
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            poly.append(QPointF(
                center.x() + radius * math.cos(angle),
                center.y() + radius * math.sin(angle)
            ))
        return poly
