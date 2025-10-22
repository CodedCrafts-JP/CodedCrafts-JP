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
from collections import deque

class Object3DGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 3D Drone Movement Visualization - Interactive Exhibition")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1e1e1e')
        
        # Set modern dark theme
        self.setup_styles()

        # Object state
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
        
        # Button press tracking for continuous movement
        self.button_pressed = {}
        self.button_repeat_delay = 50  # milliseconds

        # Create main layout
        self.create_layout()
        
        # Data for graphs with better performance using deque
        self.times = deque(maxlen=100)  # Increased buffer for smoother graphs
        self.pos_x_data = deque(maxlen=100)
        self.pos_y_data = deque(maxlen=100)
        self.pos_z_data = deque(maxlen=100)
        self.roll_data = deque(maxlen=100)
        self.pitch_data = deque(maxlen=100)
        self.yaw_data = deque(maxlen=100)

        # Start animation with higher frame rate
        self.anim = animation.FuncAnimation(self.fig_cube, self.update, interval=16, blit=False)  # ~60 FPS
        
        # Start continuous update loop
        self.continuous_update()

    def setup_styles(self):
        """Setup modern, exhibition-ready styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button styles with rounded appearance
        style.configure('Modern.TButton',
                       borderwidth=0,
                       relief="flat",
                       background="#4CAF50",
                       foreground="white",
                       font=('Segoe UI', 11, 'bold'),
                       padding=(15, 10))
        
        style.map('Modern.TButton',
                 background=[('active', '#66BB6A'),
                           ('pressed', '#388E3C')])

    def create_layout(self):
        """Create the main GUI layout"""
        # Main container with dark theme
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = tk.Label(main_frame, 
                              text="🚁 3D DRONE FLIGHT SIMULATOR",
                              font=('Arial', 18, 'bold'),
                              fg='#00E676',
                              bg='#1e1e1e')
        title_label.pack(pady=(0, 10))
        
        # Create paned window for resizable layout
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame: 3D plot and controls
        self.left_frame = tk.Frame(self.paned_window, bg='#2d2d2d', relief='raised', bd=2)
        self.paned_window.add(self.left_frame, weight=1)
        
        # 3D Plot with dark theme
        plt.style.use('dark_background')
        self.fig_cube = plt.Figure(figsize=(8, 6), facecolor='#2d2d2d')
        self.ax_cube = self.fig_cube.add_subplot(111, projection='3d')
        self.ax_cube.set_facecolor('#1a1a1a')
        self.ax_cube.set_title('3D Drone Visualization', color='white', fontsize=14, pad=20)
        
        self.canvas_cube = FigureCanvasTkAgg(self.fig_cube, master=self.left_frame)
        self.canvas_cube.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add navigation toolbar for zooming and panning
        toolbar_frame = tk.Frame(self.left_frame, bg='#2d2d2d')
        toolbar_frame.pack(fill=tk.X, padx=5)
        self.toolbar = NavigationToolbar2Tk(self.canvas_cube, toolbar_frame)
        self.toolbar.config(bg='#2d2d2d')
        self.toolbar.update()
        
        # Control panels
        self.create_control_panels()

        # Right frame: Enhanced graphs with zooming
        self.right_frame = tk.Frame(self.paned_window, bg='#2d2d2d', relief='raised', bd=2)
        self.paned_window.add(self.right_frame, weight=1)
        
        # Graph title
        graph_title = tk.Label(self.right_frame, 
                              text="📊 TELEMETRY DATA",
                              font=('Arial', 14, 'bold'),
                              fg='#00E676',
                              bg='#2d2d2d')
        graph_title.pack(pady=(5, 0))
        
        self.fig_graphs = plt.Figure(figsize=(6, 8), facecolor='#2d2d2d')
        
        # Position graph
        self.ax_pos = self.fig_graphs.add_subplot(211)
        self.ax_pos.set_facecolor('#0a0a0a')
        self.ax_pos.set_title('Position Tracking (m)', color='white', fontsize=12)
        
        # Rotation graph
        self.ax_rot = self.fig_graphs.add_subplot(212)
        self.ax_rot.set_facecolor('#0a0a0a')
        self.ax_rot.set_title('Rotation Tracking (degrees)', color='white', fontsize=12)
        
        self.canvas_graphs = FigureCanvasTkAgg(self.fig_graphs, master=self.right_frame)
        self.canvas_graphs.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add navigation toolbar for graphs (zooming feature)
        graph_toolbar_frame = tk.Frame(self.right_frame, bg='#2d2d2d')
        graph_toolbar_frame.pack(fill=tk.X, padx=5)
        self.graph_toolbar = NavigationToolbar2Tk(self.canvas_graphs, graph_toolbar_frame)
        self.graph_toolbar.config(bg='#2d2d2d')
        self.graph_toolbar.update()

    def create_control_panels(self):
        """Create enhanced control panels with modern styling"""
        control_frame = tk.Frame(self.left_frame, bg='#2d2d2d')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Translation controls
        trans_label = tk.Label(control_frame, 
                              text="🎯 TRANSLATION CONTROLS",
                              font=('Arial', 12, 'bold'),
                              fg='#2196F3',
                              bg='#2d2d2d')
        trans_label.pack(pady=(0, 5))
        
        self.button_frame_trans = tk.Frame(control_frame, bg='#2d2d2d')
        self.button_frame_trans.pack(fill=tk.X, pady=5)
        
        # Translation buttons with hold functionality
        trans_buttons = [
            ("⬅️ -X", lambda: self.adjust_velocity_x(-0.1)),
            ("➡️ +X", lambda: self.adjust_velocity_x(0.1)),
            ("⬇️ -Y", lambda: self.adjust_velocity_y(-0.1)),
            ("⬆️ +Y", lambda: self.adjust_velocity_y(0.1)),
            ("🔽 -Z", lambda: self.adjust_velocity_z(-0.1)),
            ("🔼 +Z", lambda: self.adjust_velocity_z(0.1)),
        ]
        
        for i, (text, command) in enumerate(trans_buttons):
            button = tk.Button(self.button_frame_trans, 
                             text=text,
                             font=('Arial', 9, 'bold'),
                             bg='#2196F3',
                             fg='white',
                             activebackground='#1976D2',
                             activeforeground='white',
                             relief='flat',
                             bd=0,
                             padx=10,
                             pady=8)
            button.grid(row=0, column=i, padx=3, pady=2, sticky='ew')
            
            # Bind events for continuous movement
            button.bind('<ButtonPress-1>', lambda e, cmd=command, btn=text: self.on_button_press(cmd, btn))
            button.bind('<ButtonRelease-1>', lambda e, btn=text: self.on_button_release(btn))
            
        for i in range(6):
            self.button_frame_trans.grid_columnconfigure(i, weight=1)
        
        # Rotation controls
        rot_label = tk.Label(control_frame, 
                            text="🔄 ROTATION CONTROLS",
                            font=('Arial', 12, 'bold'),
                            fg='#9C27B0',
                            bg='#2d2d2d')
        rot_label.pack(pady=(15, 5))
        
        self.button_frame_rot = tk.Frame(control_frame, bg='#2d2d2d')
        self.button_frame_rot.pack(fill=tk.X, pady=5)
        
        # Rotation buttons
        rot_buttons = [
            ("↻ +Roll", lambda: self.adjust_angular_velocity_roll(0.1)),
            ("↺ -Roll", lambda: self.adjust_angular_velocity_roll(-0.1)),
            ("⤴️ +Pitch", lambda: self.adjust_angular_velocity_pitch(0.1)),
            ("⤵️ -Pitch", lambda: self.adjust_angular_velocity_pitch(-0.1)),
            ("↪️ +Yaw", lambda: self.adjust_angular_velocity_yaw(0.1)),
            ("↩️ -Yaw", lambda: self.adjust_angular_velocity_yaw(-0.1)),
        ]
        
        for i, (text, command) in enumerate(rot_buttons):
            button = tk.Button(self.button_frame_rot,
                             text=text,
                             font=('Arial', 9, 'bold'),
                             bg='#9C27B0',
                             fg='white',
                             activebackground='#7B1FA2',
                             activeforeground='white',
                             relief='flat',
                             bd=0,
                             padx=10,
                             pady=8)
            button.grid(row=0, column=i, padx=3, pady=2, sticky='ew')
            
            # Bind events for continuous movement
            button.bind('<ButtonPress-1>', lambda e, cmd=command, btn=text: self.on_button_press(cmd, btn))
            button.bind('<ButtonRelease-1>', lambda e, btn=text: self.on_button_release(btn))
            
        for i in range(6):
            self.button_frame_rot.grid_columnconfigure(i, weight=1)
        
        # Stop button
        stop_button = tk.Button(control_frame,
                               text="🛑 EMERGENCY STOP",
                               command=self.stop_all,
                               font=('Arial', 14, 'bold'),
                               bg='#F44336',
                               fg='white',
                               activebackground='#D32F2F',
                               activeforeground='white',
                               relief='flat',
                               bd=0,
                               padx=20,
                               pady=15)
        stop_button.pack(pady=15)
        
        # Status display
        self.create_status_display(control_frame)

    def create_status_display(self, parent):
        """Create real-time status display"""
        status_frame = tk.LabelFrame(parent, 
                                   text="📡 FLIGHT STATUS",
                                   font=('Arial', 10, 'bold'),
                                   fg='#00E676',
                                   bg='#2d2d2d',
                                   bd=2)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_vars = {}
        status_items = [
            ("Position:", "pos"),
            ("Rotation:", "rot"),
            ("Velocity:", "vel"),
            ("Angular Vel:", "ang_vel")
        ]
        
        for i, (label, key) in enumerate(status_items):
            tk.Label(status_frame, text=label, 
                    font=('Arial', 9, 'bold'),
                    fg='white', bg='#2d2d2d').grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            self.status_vars[key] = tk.StringVar()
            tk.Label(status_frame, textvariable=self.status_vars[key],
                    font=('Courier', 9),
                    fg='#00E676', bg='#2d2d2d').grid(row=i, column=1, sticky='w', padx=5, pady=2)

    def on_button_press(self, command, button_name):
        """Handle button press for continuous movement"""
        self.button_pressed[button_name] = True
        command()  # Execute immediately
        self.repeat_command(command, button_name)

    def on_button_release(self, button_name):
        """Handle button release to stop continuous movement"""
        self.button_pressed[button_name] = False

    def repeat_command(self, command, button_name):
        """Repeat command while button is pressed"""
        if self.button_pressed.get(button_name, False):
            command()
            self.root.after(self.button_repeat_delay, lambda: self.repeat_command(command, button_name))

    def continuous_update(self):
        """Continuous update loop for smooth animation"""
        self.update_status_display()
        self.root.after(50, self.continuous_update)  # Update every 50ms

    def update_status_display(self):
        """Update the real-time status display"""
        self.status_vars["pos"].set(f"X:{self.posX:.2f} Y:{self.posY:.2f} Z:{self.posZ:.2f}")
        self.status_vars["rot"].set(f"R:{np.degrees(self.roll):.1f}° P:{np.degrees(self.pitch):.1f}° Y:{np.degrees(self.yaw):.1f}°")
        self.status_vars["vel"].set(f"X:{self.velocity_x:.2f} Y:{self.velocity_y:.2f} Z:{self.velocity_z:.2f}")
        self.status_vars["ang_vel"].set(f"R:{self.angular_velocity_roll:.2f} P:{self.angular_velocity_pitch:.2f} Y:{self.angular_velocity_yaw:.2f}")

    def adjust_velocity_x(self, delta):
        self.velocity_x = max(min(self.velocity_x + delta, 2.0), -2.0)  # Increased range

    def adjust_velocity_y(self, delta):
        self.velocity_y = max(min(self.velocity_y + delta, 2.0), -2.0)

    def adjust_velocity_z(self, delta):
        self.velocity_z = max(min(self.velocity_z + delta, 2.0), -2.0)

    def adjust_angular_velocity_roll(self, delta):
        self.angular_velocity_roll = max(min(self.angular_velocity_roll + delta, 2.0), -2.0)

    def adjust_angular_velocity_pitch(self, delta):
        self.angular_velocity_pitch = max(min(self.angular_velocity_pitch + delta, 2.0), -2.0)

    def adjust_angular_velocity_yaw(self, delta):
        self.angular_velocity_yaw = max(min(self.angular_velocity_yaw + delta, 2.0), -2.0)

    def stop_all(self):
        """Emergency stop - reset all velocities"""
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.angular_velocity_roll = 0
        self.angular_velocity_pitch = 0
        self.angular_velocity_yaw = 0
        
        # Clear button press states
        self.button_pressed.clear()

    def create_drone_model(self, vertices):
        """Create a more realistic drone model"""
        # Create drone body (main cube)
        faces = [
            [vertices[0], vertices[1], vertices[3], vertices[2]],  # Bottom
            [vertices[4], vertices[5], vertices[7], vertices[6]],  # Top
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
            [vertices[0], vertices[2], vertices[6], vertices[4]],  # Left
            [vertices[1], vertices[3], vertices[7], vertices[5]]   # Right
        ]
        
        # Main body with gradient-like coloring
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
        for i, face in enumerate(faces):
            poly = Poly3DCollection([face], alpha=0.8, facecolors=colors[i], 
                                  edgecolors='white', linewidths=2)
            self.ax_cube.add_collection3d(poly)
        
        # Add propeller indicators (small spheres at corners)
        prop_positions = [
            [vertices[0][0], vertices[0][1], vertices[0][2] + 0.3],
            [vertices[1][0], vertices[1][1], vertices[1][2] + 0.3],
            [vertices[2][0], vertices[2][1], vertices[2][2] + 0.3],
            [vertices[3][0], vertices[3][1], vertices[3][2] + 0.3]
        ]
        
        for pos in prop_positions:
            self.ax_cube.scatter(*pos, s=100, c='red', marker='o', alpha=0.9)

    def update(self, frame):
        """Enhanced update function with smoother animations"""
        # Time delta for smooth movement
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Apply damping for more realistic movement
        damping = 0.98
        self.velocity_x *= damping
        self.velocity_y *= damping
        self.velocity_z *= damping
        self.angular_velocity_roll *= damping
        self.angular_velocity_pitch *= damping
        self.angular_velocity_yaw *= damping

        # Update position and rotation
        self.posX += self.velocity_x * dt
        self.posY += self.velocity_y * dt
        self.posZ += self.velocity_z * dt
        self.roll += self.angular_velocity_roll * dt
        self.pitch += self.angular_velocity_pitch * dt
        self.yaw += self.angular_velocity_yaw * dt

        # Update 3D drone visualization
        self.ax_cube.clear()
        
        # Create drone geometry
        r = [-0.5, 0.5]
        vertices = np.array([[x, y, z] for x in r for y in r for z in r])
        
        # Apply rotations
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
        
        # Create enhanced drone model
        self.create_drone_model(rotated_vertices)
        
        # Enhanced 3D plot styling
        self.ax_cube.set_xlim([-8, 8])
        self.ax_cube.set_ylim([-8, 8])
        self.ax_cube.set_zlim([-8, 8])
        self.ax_cube.set_xlabel('X (meters)', color='white', fontsize=10)
        self.ax_cube.set_ylabel('Y (meters)', color='white', fontsize=10)
        self.ax_cube.set_zlabel('Z (meters)', color='white', fontsize=10)
        self.ax_cube.set_box_aspect([1, 1, 1])
        
        # Grid and styling
        self.ax_cube.grid(True, alpha=0.3)
        self.ax_cube.xaxis.pane.fill = False
        self.ax_cube.yaxis.pane.fill = False
        self.ax_cube.zaxis.pane.fill = False
        self.ax_cube.xaxis.pane.set_edgecolor('gray')
        self.ax_cube.yaxis.pane.set_edgecolor('gray')
        self.ax_cube.zaxis.pane.set_edgecolor('gray')
        self.ax_cube.xaxis.pane.set_alpha(0.1)
        self.ax_cube.yaxis.pane.set_alpha(0.1)
        self.ax_cube.zaxis.pane.set_alpha(0.1)

        # Update telemetry data
        self.times.append(current_time)
        self.pos_x_data.append(self.posX)
        self.pos_y_data.append(self.posY)
        self.pos_z_data.append(self.posZ)
        self.roll_data.append(np.degrees(self.roll))
        self.pitch_data.append(np.degrees(self.pitch))
        self.yaw_data.append(np.degrees(self.yaw))

        # Enhanced graph styling with smooth lines
        self.ax_pos.clear()
        self.ax_rot.clear()
        
        # Set dark theme for graphs
        self.ax_pos.set_facecolor('#0a0a0a')
        self.ax_rot.set_facecolor('#0a0a0a')
        
        # Grid styling
        self.ax_pos.grid(True, color='#333333', linestyle='-', alpha=0.3)
        self.ax_rot.grid(True, color='#333333', linestyle='-', alpha=0.3)
        
        if len(self.times) > 1:
            times_array = np.array(self.times)
            times_rel = times_array - times_array[0]  # Relative time
            
            # Position plots with enhanced styling
            self.ax_pos.plot(times_rel, list(self.pos_x_data), color='#FF6B6B', 
                           label='X Position', linewidth=2, alpha=0.9)
            self.ax_pos.plot(times_rel, list(self.pos_y_data), color='#4ECDC4', 
                           label='Y Position', linewidth=2, alpha=0.9)
            self.ax_pos.plot(times_rel, list(self.pos_z_data), color='#45B7D1', 
                           label='Z Position', linewidth=2, alpha=0.9)
            
            # Rotation plots
            self.ax_rot.plot(times_rel, list(self.roll_data), color='#FF6B6B', 
                           label='Roll', linewidth=2, alpha=0.9)
            self.ax_rot.plot(times_rel, list(self.pitch_data), color='#4ECDC4', 
                           label='Pitch', linewidth=2, alpha=0.9)
            self.ax_rot.plot(times_rel, list(self.yaw_data), color='#45B7D1', 
                           label='Yaw', linewidth=2, alpha=0.9)
        
        # Enhanced labels and legends
        self.ax_pos.set_ylabel('Position (m)', color='white', fontsize=10)
        self.ax_rot.set_ylabel('Rotation (°)', color='white', fontsize=10)
        self.ax_rot.set_xlabel('Time (s)', color='white', fontsize=10)
        
        # Legends with better styling
        pos_legend = self.ax_pos.legend(loc='upper right', framealpha=0.8, 
                                       facecolor='#2d2d2d', edgecolor='white')
        rot_legend = self.ax_rot.legend(loc='upper right', framealpha=0.8, 
                                       facecolor='#2d2d2d', edgecolor='white')
        
        for text in pos_legend.get_texts():
            text.set_color('white')
        for text in rot_legend.get_texts():
            text.set_color('white')
        
        # Tick colors
        self.ax_pos.tick_params(colors='white', labelsize=8)
        self.ax_rot.tick_params(colors='white', labelsize=8)
        
        self.fig_graphs.tight_layout()
        
        # Draw updates
        self.canvas_cube.draw_idle()
        self.canvas_graphs.draw_idle()

if __name__ == "__main__":
    root = tk.Tk()
    app = Object3DGUI(root)
    root.mainloop()
