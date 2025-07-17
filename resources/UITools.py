from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from resources.Tools import upgrade_pressed_button, can_afford

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
    upgrade_button.clicked.connect(lambda _, b=upgrade_button, c=cost_dict: upgrade_pressed_button(b, c, parent))

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

def create_mini_game_info_layout(parent):
    layout = QHBoxLayout()

    # Create QGroupBoxes for each QLabel
    scans_remaining_group = QGroupBox()
    detected_loot_group = QGroupBox()
    profit_group = QGroupBox()
    max_loot_value_group = QGroupBox()
    highscore_group = QGroupBox()

    # Set object name for styling
    scans_remaining_group.setObjectName("orellow-border")
    detected_loot_group.setObjectName("orellow-border")
    profit_group.setObjectName("orellow-border")
    max_loot_value_group.setObjectName("orellow-border")
    highscore_group.setObjectName("orellow-border")

    # Create layouts for each QGroupBox
    scans_remaining_layout = QVBoxLayout()
    detected_loot_layout = QVBoxLayout()
    profit_layout = QVBoxLayout()
    max_loot_value_layout = QVBoxLayout()
    highscore_layout = QVBoxLayout()

    parent.scansRemainingLabel = QLabel(f"Scans Remaining: {parent.resources.user_data['buildings']['1']['search_count']}")
    parent.detectedLootLabel = QLabel(f"Loot Remaining: {parent.resources.user_data['buildings']['1']['hidden_objects']}")
    parent.profitThisRunLabel = QLabel(f"Current Profits: <span style='color: {parent.resources.colors['orellow']};'>0 Gold</span>")
    parent.maxLootValueLabel = QLabel(f"Loot Value: Between <span style='color: {parent.resources.colors['orellow']};'>{parent.resources.user_data['buildings']['1']['min_asteroid_value']} - {parent.resources.user_data['buildings']['1']['max_asteroid_value']} Gold</span>")
    parent.highscoreLabel = QLabel(f"Highscore: <span style='color: {parent.resources.colors['orellow']};'>{parent.resources.user_data['buildings']['1']['highscore']} Gold</span>")

    parent.scansRemainingLabel.setStyleSheet("font-weight: bold;")
    parent.detectedLootLabel.setStyleSheet("font-weight: bold;")
    parent.profitThisRunLabel.setStyleSheet("font-weight: bold;")
    parent.maxLootValueLabel.setStyleSheet("font-weight: bold;")
    parent.highscoreLabel.setStyleSheet("font-weight: bold;")

    # Add QLabel to respective layouts
    scans_remaining_layout.addWidget(parent.scansRemainingLabel)
    detected_loot_layout.addWidget(parent.detectedLootLabel)
    profit_layout.addWidget(parent.profitThisRunLabel)
    max_loot_value_layout.addWidget(parent.maxLootValueLabel)
    highscore_layout.addWidget(parent.highscoreLabel)

    # Set layouts for each QGroupBox
    scans_remaining_group.setLayout(scans_remaining_layout)
    detected_loot_group.setLayout(detected_loot_layout)
    profit_group.setLayout(profit_layout)
    max_loot_value_group.setLayout(max_loot_value_layout)
    highscore_group.setLayout(highscore_layout)

    # Add QGroupBoxes to base layout
    layout.addWidget(scans_remaining_group)
    layout.addWidget(detected_loot_group)
    layout.addWidget(profit_group)
    layout.addWidget(max_loot_value_group)
    layout.addWidget(highscore_group)

    return layout