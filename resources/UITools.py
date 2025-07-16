from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

def create_upgrade_box(upgrade_id, upgrade_title, upgrade_desc_text, rank_text, cost_dict, parent):
    upgrade_box = QGroupBox(upgrade_title)
    upgrade_box.setObjectName("grey-border")
    upgrade_box.setFixedHeight(140)

    upgrade_box_layout = QVBoxLayout()

    # Top row: description + rank
    top_row = QHBoxLayout()

    desc_label = QLabel(upgrade_desc_text)
    desc_label.setWordWrap(True)
    desc_label.setStyleSheet(f"font-size: 12px; color: {parent.resources.colors['light-text']};")
    setattr(parent, f"{upgrade_id}_desc", desc_label)

    rank_label = QLabel(rank_text)
    rank_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
    setattr(parent, f"{upgrade_id}_rank", rank_label)

    top_row.addWidget(desc_label, stretch=1)
    top_row.addWidget(rank_label, stretch=0)

    cost_label = create_cost_label(parent, cost_dict)
    cost_label.setStyleSheet("font-weight: bold;")
    setattr(parent, f"{upgrade_id}_cost", cost_label)

    # print('Can Afford: ', can_afford(parent.resources.user_data['resources'], cost_dict))
    affordable = can_afford(parent.resources.user_data['resources'], cost_dict)
    if not affordable:
        upgrade_button = QPushButton("Insufficient Resources")
        upgrade_button.setObjectName("disabled")
    else:
        upgrade_button = QPushButton("Upgrade")
    setattr(parent, f"{upgrade_id}_button", upgrade_button)
    # upgrade_button.clicked.connect(getattr(parent, f"{upgrade_id}_clicked"))

    upgrade_box_layout.addLayout(top_row)
    upgrade_box_layout.addWidget(cost_label)
    upgrade_box_layout.addWidget(upgrade_button)
    upgrade_box.setLayout(upgrade_box_layout)

    return upgrade_box

def once_ui_has_been_created(parent):
    parent.map_viewer.upgrade_clicked(None, int(parent.map_viewer.planet_size/2), int(parent.map_viewer.planet_size/2))

    for button in parent.findChildren(QPushButton):
        button.setCursor(Qt.CursorShape.PointingHandCursor)

def add_padding_to_icon(icon, padding=6):
    pixmap = icon.pixmap(32, 32)
    padded_pixmap = QPixmap(pixmap.width() + padding*2, pixmap.height() + padding*2)
    padded_pixmap.fill(QColor("transparent"))
    painter = QPainter(padded_pixmap)
    painter.drawPixmap(padding, padding, pixmap)
    painter.end()

    padded_icon = QIcon(padded_pixmap)
    return padded_icon

def create_cost_label(parent, cost_dict):
    resources = parent.resources.user_data['resources']
    cost_items = []
    for resource, amount in cost_dict.items():
        owned_amount = resources.get(resource, 0)
        if amount > 0:
            color = parent.resources.colors['green'] if owned_amount >= amount else parent.resources.colors['orellow']
            cost_items.append(f"<span style='color:{color}'>{amount} {resource.capitalize()}</span>")
    cost_text = "Cost: " + ", ".join(cost_items) if cost_items else "None"
    
    return QLabel(cost_text)

def can_afford(resources, cost_dict):
    for resource, amount in cost_dict.items():
        if resources.get(resource, 0) < amount:
            return False
    return True