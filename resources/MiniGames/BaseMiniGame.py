from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import random

class SquareItem(QGraphicsRectItem):
    def __init__(self, rect, rock=None, parent=None):
        super().__init__(rect, parent)
        self.rock = rock
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        
        pen = QPen(QColor(200, 200, 200))
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setWidth(2)
        self.setPen(pen)
        
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setOpacity(1.0)
        self.clicked_callback = None

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(rect, 24, 24)
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawPath(path)

    def mousePressEvent(self, event):
        if self.clicked_callback:
            self.clicked_callback(self, self.rock)

class BaseMiniGame(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.grid_size = 5
        self.rectangle_size = 84
        self.number_of_hits_player_clicked = 0
        self.profit = 0
        self.min_gold = 1
        self.max_gold = 5

        self.scene = QGraphicsScene(self)
        # self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        try:
            background_image = QPixmap(parent.resources.resource_path('assets/starry-sky.png'))
            self.setBackgroundBrush(QBrush(background_image))
        except:
            pass

        # self.scene.setBackgroundBrush(QBrush(pixmap.scaledToHeight(self.scene.sceneRect().height(), Qt.TransformationMode.SmoothTransformation)))
        
        self.setScene(self.scene)
        self.setSceneRect(0, 0, self.grid_size*self.rectangle_size, self.grid_size*self.rectangle_size)
        self.squares = []
        self.rocks = []
        self.clicked_count = 0
        try:
            self.rock_pixmap = QPixmap(parent.resources.resource_path("assets/icons/galaxy.png")).scaled(self.rectangle_size-10, self.rectangle_size-10, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        except:
            self.rock_pixmap = QPixmap(self.rectangle_size-10, self.rectangle_size-10)
            self.rock_pixmap.fill(QColor("red"))
        self.reset_grid()

    def reset_grid(self):
        try:
            self.number_of_hidden_items = self.parent.resources.user_data['buildings']['1']['hidden_objects']
        except:
            self.number_of_hidden_items = 2

        try:
            self.number_of_attempts = self.parent.resources.user_data['buildings']['1']['search_count']
        except:
            self.number_of_attempts = 4
    
        self.scene.clear()
        self.squares = []
        self.rocks = []
        self.clicked_count = 0
        self.number_of_hits_player_clicked = 0
        self.profit = 0

        positions = [(i, j) for i in range(3) for j in range(3)]
        rock_positions = set(random.sample(positions, self.number_of_hidden_items))

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x, y = 10 + j * self.rectangle_size, 10 + i * self.rectangle_size
                rect = QRectF(x, y, self.rectangle_size-10, self.rectangle_size-10)
                rock = None
                if (i, j) in rock_positions:
                    rock = QGraphicsPixmapItem(self.rock_pixmap)
                    rock.setPos(x, y)
                    rock.setZValue(0)
                    rock.setVisible(False)
                    self.scene.addItem(rock)
                    self.rocks.append(rock)

                square = SquareItem(rect, rock)
                square.setZValue(1)
                self.scene.addItem(square)
                self.squares.append(square)
                square.clicked_callback = self.fade_square

    def fade_square(self, square, rock):
        square.setBrush(QBrush(QColor(0, 0, 0, 0)))
        self.on_square_faded(square, rock)

    def on_square_faded(self, square, rock):
        square.setVisible(False)
        if rock:
            self.number_of_hits_player_clicked += 1
            rock.setVisible(True)
            gold_earned = random.randint(self.min_gold, self.max_gold)
            self.profit += gold_earned
        self.clicked_count += 1
        if self.clicked_count == self.number_of_attempts:
            self.show_results_screen()

    def show_results_screen(self):
        overlay_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        overlay = QGraphicsRectItem(overlay_rect)
        overlay.setBrush(QBrush(QColor(0, 0, 0, 150)))
        overlay.setZValue(2)
        self.scene.addItem(overlay)

        text = f'You hit {self.number_of_hits_player_clicked} rocks!'
        text_item = QGraphicsTextItem(text, overlay)
        font = text_item.font()
        font.setPointSize(18)
        text_item.setFont(font)
        text_item.setPos(
            overlay_rect.center().x() - text_item.boundingRect().width() / 2,
            overlay_rect.center().y() - text_item.boundingRect().height() / 2 - 30
        )

        profit_text = f'Profit: '
        profit_text_item = QGraphicsTextItem(profit_text, overlay)
        profit_font = profit_text_item.font()
        profit_font.setPointSize(14)
        profit_text_item.setFont(profit_font)
        profit_text_item.setDefaultTextColor(QColor("white"))
        profit_text_item.setPos(
            overlay_rect.center().x() - profit_text_item.boundingRect().width() / 2 - 30,
            overlay_rect.center().y() - profit_text_item.boundingRect().height() / 2
        )

        profit_value_text = f'{self.profit} Gold'
        profit_value_item = QGraphicsTextItem(profit_value_text, profit_text_item)
        profit_value_font = profit_value_item.font()
        profit_value_font.setPointSize(14)
        profit_value_item.setFont(profit_value_font)
        try:
            profit_value_item.setDefaultTextColor(QColor(self.parent.resources.colors['orellow']))
        except:
            profit_value_item.setDefaultTextColor(QColor("#f7d68a"))
        profit_value_item.setPos(
            profit_text_item.boundingRect().width(),
            0
        )

        continue_text = 'Tap anywhere to continue'
        continue_text_item = QGraphicsTextItem(continue_text, overlay)
        continue_font = continue_text_item.font()
        continue_font.setPointSize(10)
        continue_text_item.setFont(continue_font)
        continue_text_item.setDefaultTextColor(QColor("grey"))
        continue_text_item.setPos(
            overlay_rect.center().x() - continue_text_item.boundingRect().width() / 2,
            overlay_rect.center().y() - continue_text_item.boundingRect().height() / 2 + 30
        )

        self.setScene(self.scene)

        def reset_on_click(event):
            self.scene.removeItem(overlay)
            self.reset_grid()

        overlay.mousePressEvent = reset_on_click

        try:
            self.parent.resources.user_data['resources']['gold'] += self.profit
            self.parent.resource_labels['gold'].setText(str(self.parent.resources.user_data['resources']['gold']))

            if self.profit > self.parent.resources.user_data['buildings']['1']['highscore']:
                self.parent.resources.user_data['buildings']['1']['highscore'] = self.profit
                self.parent.resources.save()
                highscore_text = 'New Highscore!'
                highscore_text_item = QGraphicsTextItem(highscore_text, overlay)
                continue_font = highscore_text_item.font()
                continue_font.setPointSize(16)
                highscore_text_item.setFont(continue_font)
                highscore_text_item.setDefaultTextColor(QColor(self.parent.resources.colors['green']))
                highscore_text_item.setPos(
                    overlay_rect.center().x() - highscore_text_item.boundingRect().width() / 2,
                    overlay_rect.center().y() - highscore_text_item.boundingRect().height() / 2 - 60
                )
        except:
            pass

    def wheelEvent(self, event, limited_zoom=True):
        if not limited_zoom:
            zoom_factor = 1.5 if event.angleDelta().y() > 0 else (1 / 1.5)
            self.scale(zoom_factor, zoom_factor)
            event.accept()
            return
        
        zoom_in_factor = 1.5
        zoom_out_factor = 1 / zoom_in_factor

        visible_height = self.viewport().height()
        scene_height = self.scene.sceneRect().height()

        if visible_height > scene_height:
            visible_height = scene_height

        min_scale = visible_height / scene_height
        current_scale = self.transform().m11()

        if event.angleDelta().y() > 0 and current_scale < 0.75:
            self.scale(zoom_in_factor, zoom_in_factor)
        elif event.angleDelta().y() < 0 and current_scale > 0.35:
            self.scale(zoom_out_factor, zoom_out_factor)

        event.accept()

# Example usage:
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    view = BaseMiniGame()
    view.show()
    sys.exit(app.exec())