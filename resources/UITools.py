from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

def create_upgrade_box(upgrade_id, upgrade_title, upgrade_desc_text, rank_text, cost_text, parent):
    upgrade_box = QGroupBox(upgrade_title)
    upgrade_box.setObjectName("orellow-border")
    upgrade_box.setFixedHeight(140)

    upgrade_box_layout = QVBoxLayout()

    # Top row: description + rank
    top_row = QHBoxLayout()

    desc_label = QLabel(upgrade_desc_text)
    desc_label.setWordWrap(True)
    setattr(parent, f"{upgrade_id}_desc", desc_label)

    rank_label = QLabel(rank_text)
    rank_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
    setattr(parent, f"{upgrade_id}_rank", rank_label)

    top_row.addWidget(desc_label)
    top_row.addWidget(rank_label)

    cost_label = QLabel(cost_text)
    setattr(parent, f"{upgrade_id}_cost", cost_label)

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
