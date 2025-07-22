import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib import animation
import time
import sys

class Object3DGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 3D Drone Movement Visualization - Enhanced Edition")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f8ff')  # Fresh light blue background

        # Object state (same as original)
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0
        self.angular_velocity_roll = 0.0
        self.angular_velocity_pitch = 0.0
        self.angular_velocity_yaw = 0.0
        self.last_time = time.time()

        # Button press tracking for continuous movement (NEW FEATURE)
        self.button_pressed = {}
        self.button_repeat_delay = 50  # milliseconds

        # Fresh, energetic styling
        self.setup_modern_styles()

        # Main layout
        self.paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame: 3D plot and buttons
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Title with fresh styling
        title_label = tk.Label(self.left_frame, 
                              text="🚁 3D Drone Flight Simulator",
                              font=('Segoe UI', 16, 'bold'),
                              fg='#2E86AB',
                              bg='#f0f8ff')
        title_label.grid(row=0, column=0, pady=(0, 10))

        # 3D Plot with fresh theme
        plt.style.use('default')  # Use default bright theme
        self.fig_cube = plt.Figure(figsize=(6, 5), facecolor='white')
        self.ax_cube = self.fig_cube.add_subplot(111, projection='3d')
        self.ax_cube.set_facecolor('#f8f9fa')
        self.ax_cube.set_title('3D Drone Visualization', fontsize=14, color='#2E86AB', weight='bold')
        self.canvas_cube = FigureCanvasTkAgg(self.fig_cube, master=self.left_frame)
        self.canvas_cube.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # Add navigation toolbar for zooming (NEW FEATURE)
        toolbar_frame = ttk.Frame(self.left_frame)
        toolbar_frame.grid(row=2, column=0, sticky='ew')
        self.toolbar = NavigationToolbar2Tk(self.canvas_cube, toolbar_frame)
        self.toolbar.update()

        # Button frames with fresh styling
        self.button_frame_trans = ttk.Frame(self.left_frame)
        self.button_frame_trans.grid(row=3, column=0, sticky='ew', pady=10)
        self.button_frame_rot = ttk.Frame(self.left_frame)
        self.button_frame_rot.grid(row=4, column=0, sticky='ew')

        # Create buttons with hold functionality (IMPROVED FEATURE)
        self.create_control_buttons()

        # Right frame: Enhanced graphs with zooming (NEW FEATURE)
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=1)
        
        # Graph title
        graph_title = tk.Label(self.right_frame,
                              text="📊 Real-time Telemetry Data",
                              font=('Segoe UI', 14, 'bold'),
                              fg='#A23B72',
                              bg='#f0f8ff')
        graph_title.pack(pady=(0, 10))

        self.fig_graphs = plt.Figure(figsize=(6, 6), facecolor='white')
        self.ax_pos = self.fig_graphs.add_subplot(211)
        self.ax_pos.set_facecolor('#f8f9fa')
        self.ax_pos.set_title('Position over Time', fontsize=12, color='#2E86AB')
        self.ax_rot = self.fig_graphs.add_subplot(212)
        self.ax_rot.set_facecolor('#f8f9fa')
        self.ax_rot.set_title('Rotation over Time', fontsize=12, color='#A23B72')
        self.canvas_graphs = FigureCanvasTkAgg(self.fig_graphs, master=self.right_frame)
        self.canvas_graphs.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add navigation toolbar for graphs (NEW FEATURE - ZOOMING)
        graph_toolbar_frame = ttk.Frame(self.right_frame)
        graph_toolbar_frame.pack(fill=tk.X)
        self.graph_toolbar = NavigationToolbar2Tk(self.canvas_graphs, graph_toolbar_frame)
        self.graph_toolbar.update()

        # Data for graphs (same as original but optimized)
        self.times = []
        self.pos_x_data = []
        self.pos_y_data = []
        self.pos_z_data = []
        self.roll_data = []
        self.pitch_data = []
        self.yaw_data = []
        self.max_points = 50

        # Start animation (same timing as original for smoothness)
        self.anim = animation.FuncAnimation(self.fig_cube, self.update, interval=20, blit=False)

    def setup_modern_styles(self):
        """Setup fresh, energetic modern styles"""
        style = ttk.Style()
        
        # Fresh button style - energetic blue
        style.configure('Fresh.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(10, 8))

    def create_control_buttons(self):
        """Create control buttons with hold functionality"""
        # Translation buttons with emoji and fresh colors
        trans_buttons = [
            ("⬅️ -X", lambda: self.adjust_velocity_x(-0.1)),
            ("➡️ +X", lambda: self.adjust_velocity_x(0.1)),
            ("⬇️ -Y", lambda: self.adjust_velocity_y(-0.1)),
            ("⬆️ +Y", lambda: self.adjust_velocity_y(0.1)),
            ("🔽 -Z", lambda: self.adjust_velocity_z(-0.1)),
            ("🔼 +Z", lambda: self.adjust_velocity_z(0.1)),
        ]

        # Create translation label
        trans_label = tk.Label(self.left_frame,
                              text="🎯 Movement Controls",
                              font=('Segoe UI', 12, 'bold'),
                              fg='#2E86AB',
                              bg='#f0f8ff')
        trans_label.grid(row=5, column=0, pady=(10, 5))

        for i, (text, command) in enumerate(trans_buttons):
            # Create modern button with fresh styling
            button = tk.Button(self.button_frame_trans, 
                             text=text,
                             font=('Segoe UI', 9, 'bold'),
                             bg='#4A90E2',  # Fresh blue
                             fg='white',
                             activebackground='#357ABD',
                             relief='raised',
                             bd=2,
                             padx=8,
                             pady=6,
                             cursor='hand2')
            button.grid(row=0, column=i, padx=3, pady=2, sticky='ew')
            
            # Bind events for continuous movement (NEW FEATURE)
            button.bind('<ButtonPress-1>', lambda e, cmd=command, btn=text: self.on_button_press(cmd, btn))
            button.bind('<ButtonRelease-1>', lambda e, btn=text: self.on_button_release(btn))
            
        for i in range(6):
            self.button_frame_trans.grid_columnconfigure(i, weight=1)

        # Rotation buttons with fresh styling
        rot_buttons = [
            ("🔄 +Roll", lambda: self.adjust_angular_velocity_roll(0.1)),
            ("🔄 -Roll", lambda: self.adjust_angular_velocity_roll(-0.1)),
            ("⤴️ +Pitch", lambda: self.adjust_angular_velocity_pitch(0.1)),
            ("⤵️ -Pitch", lambda: self.adjust_angular_velocity_pitch(-0.1)),
            ("↪️ +Yaw", lambda: self.adjust_angular_velocity_yaw(0.1)),
            ("↩️ -Yaw", lambda: self.adjust_angular_velocity_yaw(-0.1)),
        ]

        # Create rotation label
        rot_label = tk.Label(self.left_frame,
                            text="🔄 Rotation Controls",
                            font=('Segoe UI', 12, 'bold'),
                            fg='#A23B72',
                            bg='#f0f8ff')
        rot_label.grid(row=6, column=0, pady=(15, 5))

        for i, (text, command) in enumerate(rot_buttons):
            button = tk.Button(self.button_frame_rot,
                             text=text,
                             font=('Segoe UI', 9, 'bold'),
                             bg='#B83DBA',  # Fresh purple
                             fg='white',
                             activebackground='#9A2A9D',
                             relief='raised',
                             bd=2,
                             padx=8,
                             pady=6,
                             cursor='hand2')
            button.grid(row=0, column=i, padx=3, pady=2, sticky='ew')
            
            # Bind events for continuous movement (NEW FEATURE)
            button.bind('<ButtonPress-1>', lambda e, cmd=command, btn=text: self.on_button_press(cmd, btn))
            button.bind('<ButtonRelease-1>', lambda e, btn=text: self.on_button_release(btn))
            
        for i in range(6):
            self.button_frame_rot.grid_columnconfigure(i, weight=1)

        # Enhanced Stop button
        stop_button = tk.Button(self.left_frame,
                               text="🛑 STOP ALL",
                               command=self.stop_all,
                               font=('Segoe UI', 14, 'bold'),
                               bg='#E74C3C',  # Fresh red
                               fg='white',
                               activebackground='#C0392B',
                               relief='raised',
                               bd=3,
                               padx=20,
                               pady=10,
                               cursor='hand2')
        stop_button.grid(row=7, column=0, pady=15)

    def on_button_press(self, command, button_name):
        """Handle button press for continuous movement (NEW FEATURE)"""
        self.button_pressed[button_name] = True
        command()  # Execute immediately
        self.repeat_command(command, button_name)

    def on_button_release(self, button_name):
        """Handle button release to stop continuous movement (NEW FEATURE)"""
        self.button_pressed[button_name] = False

    def repeat_command(self, command, button_name):
        """Repeat command while button is pressed (NEW FEATURE)"""
        if self.button_pressed.get(button_name, False):
            command()
            self.root.after(self.button_repeat_delay, lambda: self.repeat_command(command, button_name))

    def adjust_velocity_x(self, delta):
        self.velocity_x = max(min(self.velocity_x + delta, 1.0), -1.0)

    def adjust_velocity_y(self, delta):
        self.velocity_y = max(min(self.velocity_y + delta, 1.0), -1.0)

    def adjust_velocity_z(self, delta):
        self.velocity_z = max(min(self.velocity_z + delta, 1.0), -1.0)

    def adjust_angular_velocity_roll(self, delta):
        self.angular_velocity_roll = max(min(self.angular_velocity_roll + delta, 1.0), -1.0)

    def adjust_angular_velocity_pitch(self, delta):
        self.angular_velocity_pitch = max(min(self.angular_velocity_pitch + delta, 1.0), -1.0)

    def adjust_angular_velocity_yaw(self, delta):
        self.angular_velocity_yaw = max(min(self.angular_velocity_yaw + delta, 1.0), -1.0)

    def stop_all(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.angular_velocity_roll = 0
        self.angular_velocity_pitch = 0
        self.angular_velocity_yaw = 0
        # Clear button press states
        self.button_pressed.clear()

    def update(self, frame):
        # Time delta for smooth movement (same as original)
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Update position and rotation (same as original)
        self.posX += self.velocity_x * dt
        self.posY += self.velocity_y * dt
        self.posZ += self.velocity_z * dt
        self.roll += self.angular_velocity_roll * dt
        self.pitch += self.angular_velocity_pitch * dt
        self.yaw += self.angular_velocity_yaw * dt

        # Update 3D cube (same as original but with fresh colors)
        self.ax_cube.clear()
        r = [-0.5, 0.5]
        vertices = np.array([[x, y, z] for x in r for y in r for z in r])
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(self.roll), -np.sin(self.roll)],
                       [0, np.sin(self.roll), np.cos(self.roll)]])
        Ry = np.array([[np.cos(self.pitch), 0, np.sin(self.pitch)],
                       [0, 1, 0],
                       [-np.sin(self.pitch), 0, np.cos(self.pitch)]])
        Rz = np.array([[np.cos(self.yaw), -np.sin(self.yaw), 0],
                       [np.sin(self.yaw), np.cos(self.yaw), 0],
                       [0, 0, 1]])
        R = Rz @ Ry @ Rx
        rotated_vertices = vertices @ R.T
        rotated_vertices += [self.posX, self.posY, self.posZ]
        
        faces = [
            [rotated_vertices[0], rotated_vertices[1], rotated_vertices[3], rotated_vertices[2]],
            [rotated_vertices[4], rotated_vertices[5], rotated_vertices[7], rotated_vertices[6]],
            [rotated_vertices[0], rotated_vertices[1], rotated_vertices[5], rotated_vertices[4]],
            [rotated_vertices[2], rotated_vertices[3], rotated_vertices[7], rotated_vertices[6]],
            [rotated_vertices[0], rotated_vertices[2], rotated_vertices[6], rotated_vertices[4]],
            [rotated_vertices[1], rotated_vertices[3], rotated_vertices[7], rotated_vertices[5]]
        ]
        
        # Fresh, energetic colors for the drone
        poly = Poly3DCollection(faces, alpha=0.8, facecolors='#FF6B6B', edgecolors='#4ECDC4', linewidths=2)
        self.ax_cube.add_collection3d(poly)
        
        self.ax_cube.set_xlim([-5, 5])
        self.ax_cube.set_ylim([-5, 5])
        self.ax_cube.set_zlim([-5, 5])
        self.ax_cube.set_xlabel('X', color='#2E86AB', fontweight='bold')
        self.ax_cube.set_ylabel('Y', color='#2E86AB', fontweight='bold')
        self.ax_cube.set_zlabel('Z', color='#2E86AB', fontweight='bold')
        self.ax_cube.set_box_aspect([1, 1, 1])

        # Update graphs (same logic as original but with fresh styling)
        self.times.append(current_time)
        self.pos_x_data.append(self.posX)
        self.pos_y_data.append(self.posY)
        self.pos_z_data.append(self.posZ)
        self.roll_data.append(np.degrees(self.roll))
        self.pitch_data.append(np.degrees(self.pitch))
        self.yaw_data.append(np.degrees(self.yaw))

        if len(self.times) > self.max_points:
            self.times.pop(0)
            self.pos_x_data.pop(0)
            self.pos_y_data.pop(0)
            self.pos_z_data.pop(0)
            self.roll_data.pop(0)
            self.pitch_data.pop(0)
            self.yaw_data.pop(0)

        # Fresh graph styling
        self.ax_pos.clear()
        self.ax_rot.clear()
        self.ax_pos.set_facecolor('#f8f9fa')
        self.ax_rot.set_facecolor('#f8f9fa')
        self.ax_pos.grid(True, color='lightgray', linestyle='--', alpha=0.7)
        self.ax_rot.grid(True, color='lightgray', linestyle='--', alpha=0.7)
        
        # Energetic colors for the graphs
        self.ax_pos.plot(self.times, self.pos_x_data, color='#FF6B6B', label='Pos X', linewidth=2.5)
        self.ax_pos.plot(self.times, self.pos_y_data, color='#4ECDC4', label='Pos Y', linewidth=2.5)
        self.ax_pos.plot(self.times, self.pos_z_data, color='#45B7D1', label='Pos Z', linewidth=2.5)
        self.ax_rot.plot(self.times, self.roll_data, color='#96CEB4', label='Roll', linewidth=2.5)
        self.ax_rot.plot(self.times, self.pitch_data, color='#FFEAA7', label='Pitch', linewidth=2.5)
        self.ax_rot.plot(self.times, self.yaw_data, color='#DDA0DD', label='Yaw', linewidth=2.5)
        
        self.ax_pos.set_ylabel('Position', color='#2E86AB', fontweight='bold')
        self.ax_rot.set_ylabel('Rotation (degrees)', color='#A23B72', fontweight='bold')
        self.ax_rot.set_xlabel('Time (s)', color='#2E86AB', fontweight='bold')
        self.ax_pos.legend(loc='upper right')
        self.ax_rot.legend(loc='upper right')
        self.fig_graphs.tight_layout()
        
        self.canvas_cube.draw()
        self.canvas_graphs.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = Object3DGUI(root)
    root.mainloop()
