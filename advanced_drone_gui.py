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
import math

class AdvancedDroneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 Advanced 3D Drone Flight Simulator - Exhibition Ready")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0a0a0a')
        self.root.state('zoomed') if sys.platform == "win32" else None
        
        # Enhanced object state with physics
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
        
        # Physics parameters
        self.gravity = -9.81
        self.drag_coefficient = 0.1
        self.thrust = 0.0
        
        # Button press tracking for continuous movement
        self.button_pressed = {}
        self.button_repeat_delay = 30  # milliseconds for smoother response
        
        # Animation state
        self.animation_running = True
        self.propeller_angle = 0.0

        # Create main layout
        self.create_layout()
        
        # Enhanced data storage with more points for smoother graphs
        self.times = deque(maxlen=200)
        self.pos_x_data = deque(maxlen=200)
        self.pos_y_data = deque(maxlen=200)
        self.pos_z_data = deque(maxlen=200)
        self.roll_data = deque(maxlen=200)
        self.pitch_data = deque(maxlen=200)
        self.yaw_data = deque(maxlen=200)
        self.velocity_data = deque(maxlen=200)
        self.altitude_data = deque(maxlen=200)

        # Start high-performance animation
        self.anim = animation.FuncAnimation(self.fig_cube, self.update, interval=16, blit=False)
        
        # Start continuous update loop
        self.continuous_update()
        
        # Bind keyboard controls
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.focus_set()

    def create_layout(self):
        """Create the advanced GUI layout"""
        # Header with animated title
        header_frame = tk.Frame(self.root, bg='#0a0a0a', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Animated title
        self.title_label = tk.Label(header_frame, 
                              text="🚁 ADVANCED DRONE FLIGHT SIMULATOR 🚁",
                              font=('Arial', 24, 'bold'),
                              fg='#00FF41',
                              bg='#0a0a0a')
        self.title_label.pack(expand=True)
        
        # Subtitle
        subtitle = tk.Label(header_frame,
                           text="Interactive Exhibition - Real-time 3D Visualization & Telemetry",
                           font=('Arial', 12),
                           fg='#00BFFF',
                           bg='#0a0a0a')
        subtitle.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create three-panel layout
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left panel: 3D visualization
        self.create_3d_panel()
        
        # Center panel: Controls
        self.create_control_panel()
        
        # Right panel: Telemetry
        self.create_telemetry_panel()

    def create_3d_panel(self):
        """Create the 3D visualization panel"""
        self.left_frame = tk.Frame(self.paned_window, bg='#1a1a1a', relief='raised', bd=3)
        self.paned_window.add(self.left_frame, weight=2)
        
        # 3D Plot with enhanced styling
        plt.style.use('dark_background')
        self.fig_cube = plt.Figure(figsize=(10, 8), facecolor='#1a1a1a')
        self.ax_cube = self.fig_cube.add_subplot(111, projection='3d')
        self.ax_cube.set_facecolor('#000000')
        self.ax_cube.set_title('3D Drone Visualization', color='#00FF41', fontsize=16, pad=20, weight='bold')
        
        self.canvas_cube = FigureCanvasTkAgg(self.fig_cube, master=self.left_frame)
        self.canvas_cube.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Enhanced navigation toolbar
        toolbar_frame = tk.Frame(self.left_frame, bg='#1a1a1a')
        toolbar_frame.pack(fill=tk.X, padx=5)
        self.toolbar = NavigationToolbar2Tk(self.canvas_cube, toolbar_frame)
        self.toolbar.config(bg='#1a1a1a')
        self.toolbar.update()

    def create_control_panel(self):
        """Create the enhanced control panel"""
        self.center_frame = tk.Frame(self.paned_window, bg='#1a1a1a', relief='raised', bd=3)
        self.paned_window.add(self.center_frame, weight=1)
        
        # Control title
        control_title = tk.Label(self.center_frame,
                               text="🎮 FLIGHT CONTROLS",
                               font=('Arial', 16, 'bold'),
                               fg='#00FF41',
                               bg='#1a1a1a')
        control_title.pack(pady=(10, 20))
        
        # Create control sections
        self.create_translation_controls()
        self.create_rotation_controls()
        self.create_advanced_controls()
        self.create_status_display()

    def create_translation_controls(self):
        """Create translation control section"""
        trans_frame = tk.LabelFrame(self.center_frame,
                                  text="🎯 TRANSLATION",
                                  font=('Arial', 12, 'bold'),
                                  fg='#00BFFF',
                                  bg='#1a1a1a',
                                  bd=2,
                                  relief='groove')
        trans_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create button grid
        button_grid = tk.Frame(trans_frame, bg='#1a1a1a')
        button_grid.pack(pady=10)
        
        # Translation buttons with enhanced styling
        trans_buttons = [
            ("⬅️", "Left", lambda: self.adjust_velocity_x(-0.15), 0, 0),
            ("➡️", "Right", lambda: self.adjust_velocity_x(0.15), 0, 2),
            ("⬆️", "Forward", lambda: self.adjust_velocity_y(0.15), 0, 1),
            ("⬇️", "Backward", lambda: self.adjust_velocity_y(-0.15), 1, 1),
            ("🔼", "Up", lambda: self.adjust_velocity_z(0.15), 2, 0),
            ("🔽", "Down", lambda: self.adjust_velocity_z(-0.15), 2, 2),
        ]
        
        for emoji, text, command, row, col in trans_buttons:
            btn_frame = tk.Frame(button_grid, bg='#1a1a1a')
            btn_frame.grid(row=row, column=col, padx=5, pady=5)
            
            button = tk.Button(btn_frame,
                             text=f"{emoji}\n{text}",
                             font=('Arial', 10, 'bold'),
                             bg='#007ACC',
                             fg='white',
                             activebackground='#005A9E',
                             relief='raised',
                             bd=3,
                             width=8,
                             height=2)
            button.pack()
            
            # Bind for continuous movement
            button.bind('<ButtonPress-1>', lambda e, cmd=command, name=text: self.on_button_press(cmd, name))
            button.bind('<ButtonRelease-1>', lambda e, name=text: self.on_button_release(name))

    def create_rotation_controls(self):
        """Create rotation control section"""
        rot_frame = tk.LabelFrame(self.center_frame,
                                text="🔄 ROTATION",
                                font=('Arial', 12, 'bold'),
                                fg='#FF6B6B',
                                bg='#1a1a1a',
                                bd=2,
                                relief='groove')
        rot_frame.pack(fill=tk.X, padx=10, pady=10)
        
        button_grid = tk.Frame(rot_frame, bg='#1a1a1a')
        button_grid.pack(pady=10)
        
        # Rotation buttons
        rot_buttons = [
            ("↻", "Roll+", lambda: self.adjust_angular_velocity_roll(0.15), 0, 0),
            ("↺", "Roll-", lambda: self.adjust_angular_velocity_roll(-0.15), 0, 1),
            ("⤴️", "Pitch+", lambda: self.adjust_angular_velocity_pitch(0.15), 1, 0),
            ("⤵️", "Pitch-", lambda: self.adjust_angular_velocity_pitch(-0.15), 1, 1),
            ("↪️", "Yaw+", lambda: self.adjust_angular_velocity_yaw(0.15), 2, 0),
            ("↩️", "Yaw-", lambda: self.adjust_angular_velocity_yaw(-0.15), 2, 1),
        ]
        
        for emoji, text, command, row, col in rot_buttons:
            button = tk.Button(button_grid,
                             text=f"{emoji}\n{text}",
                             font=('Arial', 9, 'bold'),
                             bg='#CC4125',
                             fg='white',
                             activebackground='#A0331C',
                             relief='raised',
                             bd=3,
                             width=8,
                             height=2)
            button.grid(row=row, column=col, padx=3, pady=3)
            
            # Bind for continuous movement
            button.bind('<ButtonPress-1>', lambda e, cmd=command, name=text: self.on_button_press(cmd, name))
            button.bind('<ButtonRelease-1>', lambda e, name=text: self.on_button_release(name))

    def create_advanced_controls(self):
        """Create advanced control features"""
        adv_frame = tk.LabelFrame(self.center_frame,
                                text="⚡ ADVANCED",
                                font=('Arial', 12, 'bold'),
                                fg='#FFD700',
                                bg='#1a1a1a',
                                bd=2,
                                relief='groove')
        adv_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Emergency stop
        stop_button = tk.Button(adv_frame,
                               text="🛑 EMERGENCY STOP",
                               command=self.emergency_stop,
                               font=('Arial', 14, 'bold'),
                               bg='#FF4444',
                               fg='white',
                               activebackground='#CC3333',
                               relief='raised',
                               bd=4,
                               height=2)
        stop_button.pack(pady=10, fill=tk.X, padx=10)
        
        # Reset position
        reset_button = tk.Button(adv_frame,
                                text="🏠 RESET POSITION",
                                command=self.reset_position,
                                font=('Arial', 12, 'bold'),
                                bg='#4CAF50',
                                fg='white',
                                activebackground='#45a049',
                                relief='raised',
                                bd=3)
        reset_button.pack(pady=5, fill=tk.X, padx=10)
        
        # Auto hover
        hover_button = tk.Button(adv_frame,
                                text="🚁 AUTO HOVER",
                                command=self.auto_hover,
                                font=('Arial', 12, 'bold'),
                                bg='#FF9800',
                                fg='white',
                                activebackground='#F57C00',
                                relief='raised',
                                bd=3)
        hover_button.pack(pady=5, fill=tk.X, padx=10)

    def create_status_display(self):
        """Create enhanced status display"""
        status_frame = tk.LabelFrame(self.center_frame,
                                   text="📡 FLIGHT STATUS",
                                   font=('Arial', 12, 'bold'),
                                   fg='#00FF41',
                                   bg='#1a1a1a',
                                   bd=2,
                                   relief='groove')
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Status variables
        self.status_vars = {}
        status_items = [
            ("Position (m):", "pos", "#00BFFF"),
            ("Rotation (°):", "rot", "#FF6B6B"),
            ("Velocity (m/s):", "vel", "#4ECDC4"),
            ("Angular Vel (°/s):", "ang_vel", "#FFD700"),
            ("Altitude (m):", "alt", "#FF69B4"),
            ("Speed (m/s):", "speed", "#32CD32")
        ]
        
        for i, (label, key, color) in enumerate(status_items):
            label_widget = tk.Label(status_frame, text=label,
                                  font=('Arial', 9, 'bold'),
                                  fg=color, bg='#1a1a1a')
            label_widget.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            self.status_vars[key] = tk.StringVar()
            value_widget = tk.Label(status_frame, textvariable=self.status_vars[key],
                                  font=('Courier', 9, 'bold'),
                                  fg='white', bg='#1a1a1a')
            value_widget.grid(row=i, column=1, sticky='w', padx=5, pady=2)

    def create_telemetry_panel(self):
        """Create the telemetry panel with enhanced graphs"""
        self.right_frame = tk.Frame(self.paned_window, bg='#1a1a1a', relief='raised', bd=3)
        self.paned_window.add(self.right_frame, weight=2)
        
        # Telemetry title
        telem_title = tk.Label(self.right_frame,
                              text="📊 REAL-TIME TELEMETRY",
                              font=('Arial', 16, 'bold'),
                              fg='#00FF41',
                              bg='#1a1a1a')
        telem_title.pack(pady=(10, 5))
        
        # Create figure with subplots
        self.fig_graphs = plt.Figure(figsize=(8, 10), facecolor='#1a1a1a')
        
        # Position graph
        self.ax_pos = self.fig_graphs.add_subplot(311)
        self.ax_pos.set_facecolor('#000000')
        self.ax_pos.set_title('Position Tracking', color='white', fontsize=12, weight='bold')
        
        # Rotation graph
        self.ax_rot = self.fig_graphs.add_subplot(312)
        self.ax_rot.set_facecolor('#000000')
        self.ax_rot.set_title('Rotation Tracking', color='white', fontsize=12, weight='bold')
        
        # Velocity graph
        self.ax_vel = self.fig_graphs.add_subplot(313)
        self.ax_vel.set_facecolor('#000000')
        self.ax_vel.set_title('Velocity & Altitude', color='white', fontsize=12, weight='bold')
        
        self.canvas_graphs = FigureCanvasTkAgg(self.fig_graphs, master=self.right_frame)
        self.canvas_graphs.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Graph navigation toolbar
        graph_toolbar_frame = tk.Frame(self.right_frame, bg='#1a1a1a')
        graph_toolbar_frame.pack(fill=tk.X, padx=5)
        self.graph_toolbar = NavigationToolbar2Tk(self.canvas_graphs, graph_toolbar_frame)
        self.graph_toolbar.config(bg='#1a1a1a')
        self.graph_toolbar.update()

    def on_button_press(self, command, button_name):
        """Handle button press for continuous movement"""
        self.button_pressed[button_name] = True
        command()
        self.repeat_command(command, button_name)

    def on_button_release(self, button_name):
        """Handle button release"""
        self.button_pressed[button_name] = False

    def repeat_command(self, command, button_name):
        """Repeat command while button is pressed"""
        if self.button_pressed.get(button_name, False):
            command()
            self.root.after(self.button_repeat_delay, lambda: self.repeat_command(command, button_name))

    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym.lower()
        key_commands = {
            'w': lambda: self.adjust_velocity_y(0.1),
            's': lambda: self.adjust_velocity_y(-0.1),
            'a': lambda: self.adjust_velocity_x(-0.1),
            'd': lambda: self.adjust_velocity_x(0.1),
            'q': lambda: self.adjust_velocity_z(0.1),
            'e': lambda: self.adjust_velocity_z(-0.1),
            'space': self.emergency_stop,
            'r': self.reset_position,
        }
        
        if key in key_commands:
            key_commands[key]()

    def on_key_release(self, event):
        """Handle key release"""
        pass

    def continuous_update(self):
        """Continuous update loop"""
        self.update_status_display()
        self.animate_title()
        self.root.after(50, self.continuous_update)

    def animate_title(self):
        """Animate the title color"""
        colors = ['#00FF41', '#00FF80', '#00FFBF', '#00FFFF', '#00BFFF', '#0080FF', '#0041FF']
        current_time = time.time()
        color_index = int(current_time * 2) % len(colors)
        self.title_label.config(fg=colors[color_index])

    def update_status_display(self):
        """Update status display with enhanced information"""
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2 + self.velocity_z**2)
        
        self.status_vars["pos"].set(f"X:{self.posX:.2f} Y:{self.posY:.2f} Z:{self.posZ:.2f}")
        self.status_vars["rot"].set(f"R:{np.degrees(self.roll):.1f} P:{np.degrees(self.pitch):.1f} Y:{np.degrees(self.yaw):.1f}")
        self.status_vars["vel"].set(f"X:{self.velocity_x:.2f} Y:{self.velocity_y:.2f} Z:{self.velocity_z:.2f}")
        self.status_vars["ang_vel"].set(f"R:{np.degrees(self.angular_velocity_roll):.1f} P:{np.degrees(self.angular_velocity_pitch):.1f} Y:{np.degrees(self.angular_velocity_yaw):.1f}")
        self.status_vars["alt"].set(f"{self.posZ:.2f}")
        self.status_vars["speed"].set(f"{speed:.2f}")

    def adjust_velocity_x(self, delta):
        self.velocity_x = max(min(self.velocity_x + delta, 3.0), -3.0)

    def adjust_velocity_y(self, delta):
        self.velocity_y = max(min(self.velocity_y + delta, 3.0), -3.0)

    def adjust_velocity_z(self, delta):
        self.velocity_z = max(min(self.velocity_z + delta, 3.0), -3.0)

    def adjust_angular_velocity_roll(self, delta):
        self.angular_velocity_roll = max(min(self.angular_velocity_roll + delta, 3.0), -3.0)

    def adjust_angular_velocity_pitch(self, delta):
        self.angular_velocity_pitch = max(min(self.angular_velocity_pitch + delta, 3.0), -3.0)

    def adjust_angular_velocity_yaw(self, delta):
        self.angular_velocity_yaw = max(min(self.angular_velocity_yaw + delta, 3.0), -3.0)

    def emergency_stop(self):
        """Emergency stop - reset all velocities"""
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.angular_velocity_roll = 0
        self.angular_velocity_pitch = 0
        self.angular_velocity_yaw = 0
        self.button_pressed.clear()

    def reset_position(self):
        """Reset drone to origin"""
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.emergency_stop()

    def auto_hover(self):
        """Activate auto-hover mode"""
        self.velocity_z = -self.posZ * 0.1  # Gentle return to zero altitude
        self.velocity_x *= 0.5
        self.velocity_y *= 0.5
        self.angular_velocity_roll *= 0.5
        self.angular_velocity_pitch *= 0.5
        self.angular_velocity_yaw *= 0.5

    def create_enhanced_drone_model(self, vertices):
        """Create a more realistic and detailed drone model"""
        # Main body
        faces = [
            [vertices[0], vertices[1], vertices[3], vertices[2]],
            [vertices[4], vertices[5], vertices[7], vertices[6]],
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[0], vertices[2], vertices[6], vertices[4]],
            [vertices[1], vertices[3], vertices[7], vertices[5]]
        ]
        
        # Enhanced coloring with gradient effect
        colors = ['#FF1744', '#FF5722', '#FF9800', '#FFC107', '#4CAF50', '#2196F3']
        
        for i, face in enumerate(faces):
            poly = Poly3DCollection([face], alpha=0.9, facecolors=colors[i], 
                                  edgecolors='white', linewidths=2.5)
            self.ax_cube.add_collection3d(poly)
        
        # Animated propellers
        self.propeller_angle += 0.5
        prop_positions = [
            [vertices[0][0], vertices[0][1], vertices[0][2] + 0.4],
            [vertices[1][0], vertices[1][1], vertices[1][2] + 0.4],
            [vertices[2][0], vertices[2][1], vertices[2][2] + 0.4],
            [vertices[3][0], vertices[3][1], vertices[3][2] + 0.4]
        ]
        
        # Draw spinning propellers
        for i, pos in enumerate(prop_positions):
            # Propeller blades
            blade_length = 0.3
            angle = self.propeller_angle + i * np.pi/2
            
            x1 = pos[0] + blade_length * np.cos(angle)
            y1 = pos[1] + blade_length * np.sin(angle)
            x2 = pos[0] - blade_length * np.cos(angle)
            y2 = pos[1] - blade_length * np.sin(angle)
            
            self.ax_cube.plot([x1, x2], [y1, y2], [pos[2], pos[2]], 
                            color='yellow', linewidth=4, alpha=0.8)
            
            # Propeller hubs
            self.ax_cube.scatter(*pos, s=150, c='red', marker='o', alpha=1.0, edgecolors='white')
        
        # Add LED lights
        led_positions = [
            [vertices[0][0]-0.2, vertices[0][1]-0.2, vertices[0][2]],
            [vertices[1][0]+0.2, vertices[1][1]-0.2, vertices[1][2]],
            [vertices[2][0]-0.2, vertices[2][1]+0.2, vertices[2][2]],
            [vertices[3][0]+0.2, vertices[3][1]+0.2, vertices[3][2]]
        ]
        
        led_colors = ['red', 'green', 'blue', 'white']
        for pos, color in zip(led_positions, led_colors):
            self.ax_cube.scatter(*pos, s=80, c=color, marker='*', alpha=0.9)

    def update(self, frame):
        """Enhanced update function with physics simulation"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Enhanced physics with drag and gravity
        drag = self.drag_coefficient
        
        # Apply drag to velocities
        self.velocity_x *= (1 - drag * dt)
        self.velocity_y *= (1 - drag * dt)
        self.velocity_z *= (1 - drag * dt)
        
        # Apply drag to angular velocities
        self.angular_velocity_roll *= (1 - drag * dt)
        self.angular_velocity_pitch *= (1 - drag * dt)
        self.angular_velocity_yaw *= (1 - drag * dt)
        
        # Apply gravity (simplified)
        if self.posZ > -10:  # Ground level check
            self.velocity_z += self.gravity * dt * 0.01  # Reduced gravity for demo

        # Update positions
        self.posX += self.velocity_x * dt
        self.posY += self.velocity_y * dt
        self.posZ += self.velocity_z * dt
        
        # Update rotations
        self.roll += self.angular_velocity_roll * dt
        self.pitch += self.angular_velocity_pitch * dt
        self.yaw += self.angular_velocity_yaw * dt

        # Ground collision
        if self.posZ < -10:
            self.posZ = -10
            self.velocity_z = max(0, self.velocity_z)

        # Update 3D visualization
        self.ax_cube.clear()
        
        # Create drone geometry
        r = [-0.6, 0.6]
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
        self.create_enhanced_drone_model(rotated_vertices)
        
        # Enhanced 3D plot styling
        self.ax_cube.set_xlim([-12, 12])
        self.ax_cube.set_ylim([-12, 12])
        self.ax_cube.set_zlim([-12, 12])
        self.ax_cube.set_xlabel('X (meters)', color='#00BFFF', fontsize=11, weight='bold')
        self.ax_cube.set_ylabel('Y (meters)', color='#00BFFF', fontsize=11, weight='bold')
        self.ax_cube.set_zlabel('Z (meters)', color='#00BFFF', fontsize=11, weight='bold')
        self.ax_cube.set_box_aspect([1, 1, 1])
        
        # Enhanced grid and environment
        self.ax_cube.grid(True, alpha=0.3, color='#333333')
        
        # Ground plane
        xx, yy = np.meshgrid(np.linspace(-12, 12, 10), np.linspace(-12, 12, 10))
        zz = np.full_like(xx, -10)
        self.ax_cube.plot_surface(xx, yy, zz, alpha=0.1, color='green')
        
        # Axis styling
        self.ax_cube.tick_params(colors='white', labelsize=9)
        
        # Update telemetry data
        self.times.append(current_time)
        self.pos_x_data.append(self.posX)
        self.pos_y_data.append(self.posY)
        self.pos_z_data.append(self.posZ)
        self.roll_data.append(np.degrees(self.roll))
        self.pitch_data.append(np.degrees(self.pitch))
        self.yaw_data.append(np.degrees(self.yaw))
        
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2 + self.velocity_z**2)
        self.velocity_data.append(speed)
        self.altitude_data.append(self.posZ)

        # Update graphs
        self.update_telemetry_graphs()
        
        # Draw updates
        self.canvas_cube.draw_idle()
        self.canvas_graphs.draw_idle()

    def update_telemetry_graphs(self):
        """Update all telemetry graphs with enhanced styling"""
        if len(self.times) < 2:
            return
            
        times_array = np.array(self.times)
        times_rel = times_array - times_array[0]
        
        # Clear all graphs
        self.ax_pos.clear()
        self.ax_rot.clear()
        self.ax_vel.clear()
        
        # Set dark backgrounds
        for ax in [self.ax_pos, self.ax_rot, self.ax_vel]:
            ax.set_facecolor('#000000')
            ax.grid(True, color='#333333', linestyle='-', alpha=0.3)
            ax.tick_params(colors='white', labelsize=8)
        
        # Position plots
        self.ax_pos.plot(times_rel, list(self.pos_x_data), color='#FF6B6B', 
                        label='X Position', linewidth=2.5, alpha=0.9)
        self.ax_pos.plot(times_rel, list(self.pos_y_data), color='#4ECDC4', 
                        label='Y Position', linewidth=2.5, alpha=0.9)
        self.ax_pos.plot(times_rel, list(self.pos_z_data), color='#45B7D1', 
                        label='Z Position', linewidth=2.5, alpha=0.9)
        
        # Rotation plots
        self.ax_rot.plot(times_rel, list(self.roll_data), color='#FF6B6B', 
                        label='Roll', linewidth=2.5, alpha=0.9)
        self.ax_rot.plot(times_rel, list(self.pitch_data), color='#4ECDC4', 
                        label='Pitch', linewidth=2.5, alpha=0.9)
        self.ax_rot.plot(times_rel, list(self.yaw_data), color='#45B7D1', 
                        label='Yaw', linewidth=2.5, alpha=0.9)
        
        # Velocity and altitude plots
        self.ax_vel.plot(times_rel, list(self.velocity_data), color='#FFD700', 
                        label='Speed', linewidth=2.5, alpha=0.9)
        self.ax_vel.plot(times_rel, list(self.altitude_data), color='#FF69B4', 
                        label='Altitude', linewidth=2.5, alpha=0.9)
        
        # Enhanced labels and legends
        self.ax_pos.set_ylabel('Position (m)', color='white', fontsize=10, weight='bold')
        self.ax_rot.set_ylabel('Rotation (°)', color='white', fontsize=10, weight='bold')
        self.ax_vel.set_ylabel('Speed/Alt', color='white', fontsize=10, weight='bold')
        self.ax_vel.set_xlabel('Time (s)', color='white', fontsize=10, weight='bold')
        
        # Styled legends
        for ax in [self.ax_pos, self.ax_rot, self.ax_vel]:
            legend = ax.legend(loc='upper right', framealpha=0.9, 
                             facecolor='#1a1a1a', edgecolor='#333333')
            for text in legend.get_texts():
                text.set_color('white')
                text.set_fontsize(8)
        
        self.fig_graphs.tight_layout()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedDroneGUI(root)
    root.mainloop()
