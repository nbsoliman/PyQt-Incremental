from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluPerspective
from PIL import Image, ImageDraw, ImageFilter
import qdarktheme
# from generate_textures import generate_realistic_planet_texture
# from noise import pnoise2, pnoise3
import sys, os, uuid
import math, random

# def generate_planet_texture(size=2048, save_dir="assets"):
#     if not isinstance(size, int) or size <= 0:
#         raise ValueError("size must be a positive integer.")

#     # Ensure the save directory exists
#     os.makedirs(save_dir, exist_ok=True)

#     # Generate a unique ID for the texture
#     unique_id = str(uuid.uuid4())  # Create a UUID4 string
#     file_path = os.path.join(save_dir, f"{unique_id}_texture.jpg")

#     # Create the texture image
#     image = Image.new("RGB", (size, size), "black")
#     draw = ImageDraw.Draw(image)

#     # Generate random base color for the planet
#     base_color = (
#         random.randint(50, 200),  # Red
#         random.randint(50, 200),  # Green
#         random.randint(50, 200)   # Blue
#     )

#     # Draw base gradient
#     for y in range(size):
#         gradient_color = tuple(int(c * (y / size)) for c in base_color)
#         draw.line([(0, y), (size, y)], fill=gradient_color)

#     # Add random patterns
#     for _ in range(100):  # Number of patterns
#         x = random.randint(0, size - 1)
#         y = random.randint(0, size - 1)
#         radius = random.randint(5, size // 8)
#         pattern_color = tuple(
#             min(255, int(c * random.uniform(0.5, 1.5))) for c in base_color
#         )
#         draw.ellipse(
#             [x - radius, y - radius, x + radius, y + radius],
#             fill=pattern_color,
#             outline=None,
#         )

#     # Add some blur for smoothness
#     image = image.filter(ImageFilter.GaussianBlur(radius=2))

#     # Save the image as a .jpg
#     image.save(file_path, "JPEG")

#     return file_path

def generate_planet_texture(size=2048, save_dir="assets"):
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer.")

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Generate a unique ID for the texture
    unique_id = str(uuid.uuid4())  # Create a UUID4 string
    file_path = os.path.join(save_dir, f"{unique_id}_texture.jpg")

    # Create the texture image
    image = Image.new("RGB", (size, size), "black")
    draw = ImageDraw.Draw(image)

    # Generate a base color palette with close color values
    base_color = (
        random.randint(100, 150),  # Red
        random.randint(100, 150),  # Green
        random.randint(100, 150)   # Blue
    )

    # Draw subtle gradient background
    for y in range(size):
        gradient_color = tuple(
            int(c * (0.7 + 0.3 * (y / size))) for c in base_color
        )
        draw.line([(0, y), (size, y)], fill=gradient_color)

    # Add smooth random patterns
    overlay = Image.new("RGB", (size, size), "black")
    overlay_draw = ImageDraw.Draw(overlay)

    for _ in range(150):  # Number of patterns
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        radius = random.randint(50, size // 6)
        pattern_color = tuple(
            min(255, int(c * random.uniform(0.8, 1.2))) for c in base_color
        )
        overlay_draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=pattern_color
        )

    # Blur overlay to eliminate hard edges
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=80))

    # Blend the overlay with the base gradient
    image = Image.blend(image, overlay, alpha=0.6)

    # Final blur to create a seamless mirage effect
    image = image.filter(ImageFilter.GaussianBlur(radius=3))

    # Save the image as a .jpg
    image.save(file_path, "JPEG")

    return file_path

class Planet3DWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.angle_x = 0
        self.angle_y = 0
        self.last_mouse_pos = None
        self.zoom = -15.0
        self.textures = {}
        self.lock_controls = False
        self.toggle_autopan()

    def load_texture(self, image_path):
        img = Image.open(image_path)
        img_data = img.convert("RGB").tobytes()
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture_id

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        # Load textures
        self.textures['space'] = self.load_texture("assets/space_texture1.jpg")  # Background
        self.textures['sun'] = self.load_texture("assets/sun_texture.jpg")      # Sun
        # self.textures['earth'] = self.load_texture("assets/saturn.jpg")  # Earth
        self.textures['planet1'] = self.load_texture("assets/planet1.jpg")
        self.textures['planet2'] = self.load_texture("assets/planet2.jpg")
        self.textures['planet3'] = self.load_texture("assets/planet3.jpg")
        self.textures['planet4'] = self.load_texture("assets/planet4.jpg")

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / height if height > 0 else 1
        gluPerspective(45, aspect, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        self.draw_background()
        self.draw_planets()

    def draw_background(self):
        glBindTexture(GL_TEXTURE_2D, self.textures['space'])

        # Draw a large sphere surrounding the camera
        self.bg_radius = 50.0  # Large enough to surround the scene
        slices = 40
        stacks = 40

        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)

            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)

            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)

                # Texture coordinates flipped for inside-out sphere
                glTexCoord2f(j / slices, 1 - (i / stacks))
                glVertex3f(x * zr0 * self.bg_radius, y * zr0 * self.bg_radius, z0 * self.bg_radius)

                glTexCoord2f(j / slices, 1 - ((i + 1) / stacks))
                glVertex3f(x * zr1 * self.bg_radius, y * zr1 * self.bg_radius, z1 * self.bg_radius)
            glEnd()

    def draw_planets(self):
        # Draw the "Sun"
        glBindTexture(GL_TEXTURE_2D, self.textures['planet2'])
        glPushMatrix()
        self.draw_sphere(1.5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, self.textures['sun'])
        glPushMatrix()
        glRotatef(55, 0, 1, 0)
        glTranslatef(35.0, 0, 0)
        self.draw_sphere(3.5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, self.textures['planet1'])
        glPushMatrix()
        glRotatef(70, 0, 1, 0)
        glTranslatef(5.0, 7, 10)
        self.draw_sphere(0.7)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, self.textures['planet3'])
        glPushMatrix()
        glRotatef(110, 0, 1, 0)
        glTranslatef(12.0, 12, 0)
        self.draw_sphere(1.2)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, self.textures['planet4'])
        glPushMatrix()
        glRotatef(30, 0, 1, 0)
        glTranslatef(20.0, -12, 0)
        self.draw_sphere(2.1)
        glPopMatrix()

    def draw_sphere(self, radius, slices=20, stacks=20):
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)

            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)

            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)

                glTexCoord2f(j / slices, i / stacks)
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)

                glTexCoord2f(j / slices, (i + 1) / stacks)
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
            glEnd()

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.position()

    def mouseMoveEvent(self, event):
        if not self.lock_controls:
            if self.last_mouse_pos is not None:
                dx = event.position().x() - self.last_mouse_pos.x()
                dy = event.position().y() - self.last_mouse_pos.y()
                self.angle_x += dy
                self.angle_y += dx
                self.update()
            self.last_mouse_pos = event.position()

    def wheelEvent(self, event):
        if not self.lock_controls:
            # Set minimum and maximum zoom levels to stay within the skybox
            min_zoom = -self.bg_radius + 5.0  # Prevent the camera from zooming out of the skybox
            max_zoom = -5.0           # Allow zooming in but keep a reasonable limit

            self.zoom += event.angleDelta().y() / 120.0
            self.zoom = max(min_zoom, min(self.zoom, max_zoom))  # Clamp the zoom level
            self.update()
    
    def toggle_autopan(self):
        if hasattr(self, 'autopan_timer') and self.autopan_timer.isActive():
            self.autopan_timer.stop()
            self.lock_controls = False
        else:
            self.autopan_timer = QTimer(self)
            self.autopan_timer.timeout.connect(self.autopan)
            self.autopan_timer.start(33)  # 30fps -> 1000ms/30fps = ~33ms per frame
            self.lock_controls = True

    def autopan(self):
        self.angle_y += 0.5
        self.angle_x += 0.1
        self.update()
# self.planet_widget = Planet3DWidget()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("3D Space with Textured Planets")
#         # self.showFullScreen()
#         self.resize(1080, 720)

#         # Main layout
#         backdrop_layout = QVBoxLayout()
#         backdrop_layout.setContentsMargins(0, 0, 0, 0)
#         backdrop_layout.setSpacing(0)

#         # Main widget for the 3D content
#         widget = QWidget()
#         widget.setLayout(backdrop_layout)
#         self.setCentralWidget(widget)

#         # 3D rendering widget
#         self.planet_widget = Planet3DWidget()
#         backdrop_layout.addWidget(self.planet_widget)

#         self.create_overlay_layout()

#     def create_overlay_layout(self):
#         # Overlay container
#         overlay_layout = QVBoxLayout()
#         overlay_layout.setContentsMargins(0, 0, 0, 0)
#         overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         overlay_frame = QFrame()
#         overlay_frame.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(250, 0, 0, 180);  /* Semi-transparent black */
#                 border-radius: 10px;
#             }
#         """)

#         overlay_content_layout = QVBoxLayout()
#         overlay_content_layout.setContentsMargins(10, 10, 10, 10)
#         overlay_content_layout.setSpacing(10)

#         overlay_label = QLabel("Overlay Text")
#         overlay_label.setStyleSheet("color: white; font-size: 18px;")
#         overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         overlay_button = QPushButton("Button 1")
#         overlay_button.setStyleSheet("padding: 10px; font-size: 16px;")

#         overlay_button2 = QPushButton("Button 2")
#         overlay_button2.setStyleSheet("padding: 10px; font-size: 16px;")

#         overlay_content_layout.addWidget(overlay_label)
#         overlay_content_layout.addWidget(overlay_button)
#         overlay_content_layout.addWidget(overlay_button2)
#         overlay_content_layout.addStretch()  # Add stretch to center items

#         overlay_frame.setLayout(overlay_content_layout)
#         overlay_layout.addWidget(overlay_frame)
#         overlay_widget = QWidget()
#         overlay_widget.setLayout(overlay_layout)
#         # overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Ignore mouse events
#         # overlay_widget.setParent(self)

#         overlay_widget.resize(self.size())
#         overlay_widget.move(0, 0)
#         return overlay_layout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Space with Textured Planets")
        self.resize(1080, 720)
        # self.showFullScreen()

        # Main layout
        self.backdrop_layout = QVBoxLayout()
        self.backdrop_layout.setContentsMargins(0, 0, 0, 0)
        self.backdrop_layout.setSpacing(0)

        # Main widget for the 3D content
        widget = QWidget()
        widget.setLayout(self.backdrop_layout)
        self.setCentralWidget(widget)

        # Placeholder for your 3D widget
        # self.planet_widget = self.create_planet_widget()
        self.planet_widget = Planet3DWidget()
        self.backdrop_layout.addWidget(self.planet_widget)

        # Create the overlay layout
        self.overlay_widget = self.create_overlay_layout()

        # Ensure overlay stays floating on resize
        self.resizeEvent = self.on_resize

    def create_overlay_layout(self):
        # Overlay container
        overlay_layout = QVBoxLayout()
        overlay_layout.setContentsMargins(10, 10, 10, 10)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overlay_frame = QFrame()
        overlay_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0);  /* Semi-transparent black */
                border-radius: 10px;
            }
        """)
        overlay_frame.setFixedWidth(300)  # Set a fixed width for the overlay

        overlay_content_layout = QVBoxLayout()
        overlay_content_layout.setContentsMargins(10, 10, 10, 10)
        overlay_content_layout.setSpacing(10)

        overlay_label = QLabel("Right Overlay")
        overlay_label.setStyleSheet("color: white; font-size: 18px;")
        overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overlay_button1 = QPushButton("New Game")
        overlay_button1.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 10);  /* Semi-transparent white */
                border: 1px solid rgba(255, 255, 255, 80);  /* Light border for the glass effect */
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;  /* Text color */
            }
            QPushButton:hover {
                background-color: rgba(155, 155, 255, 20);  /* Slightly brighter on hover */
            }
        """)

        overlay_button2 = QPushButton("Load Game")
        overlay_button2.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 10);  /* Semi-transparent white */
                border: 1px solid rgba(255, 255, 255, 80);  /* Light border for the glass effect */
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;  /* Text color */
            }
            QPushButton:hover {
                background-color: rgba(155, 155, 255, 20);  /* Slightly brighter on hover */
            }
        """)

        overlay_content_layout.addWidget(overlay_label)
        overlay_content_layout.addWidget(overlay_button1)
        overlay_content_layout.addWidget(overlay_button2)
        overlay_content_layout.addStretch()  # Add stretch to center items

        overlay_frame.setLayout(overlay_content_layout)
        overlay_layout.addWidget(overlay_frame)

        overlay_widget = QWidget(self)
        overlay_widget.setLayout(overlay_layout)
        overlay_widget.setGeometry(self.width() - 110, 50, 300, 200)  # Initial position
        overlay_widget.show()

        return overlay_widget

    def on_resize(self, event):
        """Update the position and size of the overlay on window resize."""
        if self.overlay_widget:
            self.overlay_widget.setGeometry(self.width() - 310, 50, 300, 200)
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
