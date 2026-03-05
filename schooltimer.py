import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, time, timedelta
import threading
import time as time_module
from plyer import notification
import sys
import json
import xml.etree.ElementTree as ET
import os
import pickle

class SchoolDayTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("School Day Timers")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.period_color = "#e74c3c"
        self.weekend_color = "#27ae60"
        self.template_bg = "#34495e"
        
        self.root.configure(bg=self.bg_color)
        
        self.config_file = "school_timer_config.pkl"
        self.current_timetable_file = None
        self.timetable = None
        
        self.load_config()
        if not self.timetable:
            self.create_default_timetable()
        
        self.create_widgets()
        self.update_timers()
    
    def save_config(self):
        try:
            config = {
                'current_timetable_file': self.current_timetable_file
            }
            with open(self.config_file, 'wb') as f:
                pickle.dump(config, f)
        except:
            pass
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'rb') as f:
                    config = pickle.load(f)
                    self.current_timetable_file = config.get('current_timetable_file')
                    if self.current_timetable_file and os.path.exists(self.current_timetable_file):
                        if self.current_timetable_file.endswith('.json'):
                            self.timetable = self.load_json_timetable(self.current_timetable_file, show_error=False)
                        elif self.current_timetable_file.endswith('.xml'):
                            self.timetable = self.load_xml_timetable(self.current_timetable_file, show_error=False)
        except:
            pass
    
    def create_default_timetable(self):
        self.timetable = {
            'Monday': {
                'periods': [
                    {'name': 'P1 - 9HPE', 'start': time(8, 45), 'end': time(9, 40), 'room': 'TIND'},
                    {'name': 'P2 - 9ENG', 'start': time(9, 40), 'end': time(10, 40), 'room': 'M205'},
                    {'name': 'Break 1', 'start': time(10, 40), 'end': time(11, 0)},
                    {'name': 'P3 - 9FIN', 'start': time(11, 0), 'end': time(12, 0), 'room': 'E102'},
                    {'name': 'Rōpū', 'start': time(12, 0), 'end': time(12, 20), 'room': 'D224'},
                    {'name': 'P4 - 9DTE', 'start': time(12, 20), 'end': time(13, 20), 'room': 'COM3'},
                    {'name': 'Break 2', 'start': time(13, 20), 'end': time(14, 20)},
                    {'name': 'P5 - 9SST', 'start': time(14, 20), 'end': time(15, 20), 'room': 'M408'}
                ]
            },
            'Tuesday': {
                'periods': [
                    {'name': 'P1 - 9DTE', 'start': time(8, 45), 'end': time(9, 40), 'room': 'COM3'},
                    {'name': 'P2 - 9HPE', 'start': time(9, 40), 'end': time(10, 40), 'room': 'TIND'},
                    {'name': 'Break 1', 'start': time(10, 40), 'end': time(11, 0)},
                    {'name': 'P3 - 9CHI', 'start': time(11, 0), 'end': time(12, 0), 'room': 'T203'},
                    {'name': 'Rōpū', 'start': time(12, 0), 'end': time(12, 20), 'room': 'D224'},
                    {'name': 'P4 - 9MAO', 'start': time(12, 20), 'end': time(13, 20), 'room': 'TKA'},
                    {'name': 'Break 2', 'start': time(13, 20), 'end': time(14, 20)},
                    {'name': 'P5 - 9SCI', 'start': time(14, 20), 'end': time(15, 20), 'room': 'S404'}
                ]
            },
            'Wednesday': {
                'periods': [
                    {'name': 'P1 - 9HPE', 'start': time(9, 30), 'end': time(10, 20), 'room': 'R3'},
                    {'name': 'P2 - 9SST', 'start': time(10, 20), 'end': time(11, 10), 'room': 'M409'},
                    {'name': 'Break 1', 'start': time(11, 10), 'end': time(11, 30)},
                    {'name': 'P3 - 9MAT', 'start': time(11, 30), 'end': time(12, 20), 'room': 'M310'},
                    {'name': 'P4 - 9SCI', 'start': time(12, 20), 'end': time(13, 20), 'room': 'S403'},
                    {'name': 'Break 2', 'start': time(13, 20), 'end': time(14, 20)},
                    {'name': 'P5 - 9ENG', 'start': time(14, 20), 'end': time(15, 20), 'room': 'M205'}
                ]
            },
            'Thursday': {
                'periods': [
                    {'name': 'P1 - 9SST', 'start': time(8, 45), 'end': time(9, 40), 'room': 'M408'},
                    {'name': 'P2 - 9MAT', 'start': time(9, 40), 'end': time(10, 40), 'room': 'M310'},
                    {'name': 'Break 1', 'start': time(10, 40), 'end': time(11, 0)},
                    {'name': 'P3 - 9MAO', 'start': time(11, 0), 'end': time(12, 0), 'room': 'TKA'},
                    {'name': 'Rōpū', 'start': time(12, 0), 'end': time(12, 20), 'room': 'D224'},
                    {'name': 'P4 - 9ART', 'start': time(12, 20), 'end': time(13, 20), 'room': 'D201'},
                    {'name': 'Break 2', 'start': time(13, 20), 'end': time(14, 20)},
                    {'name': 'P5 - 9FIN', 'start': time(14, 20), 'end': time(15, 20), 'room': 'R6'}
                ]
            },
            'Friday': {
                'periods': [
                    {'name': 'P1 - 9SCI', 'start': time(8, 45), 'end': time(9, 40), 'room': 'S403'},
                    {'name': 'P2 - 9ART', 'start': time(9, 40), 'end': time(10, 40), 'room': 'D201'},
                    {'name': 'Break 1', 'start': time(10, 40), 'end': time(11, 0)},
                    {'name': 'P3 - 9CHI', 'start': time(11, 0), 'end': time(12, 0), 'room': 'T203'},
                    {'name': 'Rōpū', 'start': time(12, 0), 'end': time(12, 20), 'room': 'D224'},
                    {'name': 'P4 - 9MAT', 'start': time(12, 20), 'end': time(13, 20), 'room': 'M310'},
                    {'name': 'Break 2', 'start': time(13, 20), 'end': time(14, 20)},
                    {'name': 'P5 - 9ENG', 'start': time(14, 20), 'end': time(15, 20), 'room': 'M205'}
                ]
            }
        }
    
    def time_from_string(self, time_str):
        hour, minute = map(int, time_str.split(':'))
        return time(hour, minute)
    
    def load_json_timetable(self, filename, show_error=True):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            
            for day in data:
                for period in data[day]['periods']:
                    if 'start' in period and isinstance(period['start'], str):
                        period['start'] = self.time_from_string(period['start'])
                    if 'end' in period and isinstance(period['end'], str):
                        period['end'] = self.time_from_string(period['end'])
            
            return data
        except Exception as e:
            if show_error:
                messagebox.showerror("Error", f"Failed to load JSON: {str(e)}")
            return None
    
    def load_xml_timetable(self, filename, show_error=True):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            timetable = {}
            
            for day_elem in root.findall('day'):
                day_name = day_elem.get('name')
                if day_name:
                    periods = []
                    for period_elem in day_elem.findall('period'):
                        period = {}
                        for elem in period_elem:
                            if elem.tag in ['start', 'end']:
                                period[elem.tag] = self.time_from_string(elem.text)
                            else:
                                period[elem.tag] = elem.text
                        periods.append(period)
                    timetable[day_name] = {'periods': periods}
            
            return timetable
        except Exception as e:
            if show_error:
                messagebox.showerror("Error", f"Failed to load XML: {str(e)}")
            return None
    
    def upload_timetable(self):
        file_types = [
            ('JSON files', '*.json'),
            ('XML files', '*.xml'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select timetable file",
            filetypes=file_types
        )
        
        if filename:
            if filename.endswith('.json'):
                new_timetable = self.load_json_timetable(filename)
            elif filename.endswith('.xml'):
                new_timetable = self.load_xml_timetable(filename)
            else:
                messagebox.showerror("Error", "Unsupported file format")
                return
            
            if new_timetable:
                self.timetable = new_timetable
                self.current_timetable_file = filename
                self.save_config()
                messagebox.showinfo("Success", "Timetable loaded successfully!")
                self.update_status_label(f"Loaded: {os.path.basename(filename)}")
    
    def save_template(self):
        day = self.day_var.get()
        period_name = self.period_name_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        room = self.room_entry.get()
        
        if not all([period_name, start_time, end_time]):
            messagebox.showerror("Error", "Period name, start time, and end time are required!")
            return
        
        try:
            start = self.time_from_string(start_time)
            end = self.time_from_string(end_time)
        except:
            messagebox.showerror("Error", "Invalid time format! Use HH:MM (e.g., 08:45)")
            return
        
        if day not in self.timetable:
            self.timetable[day] = {'periods': []}
        
        new_period = {'name': period_name, 'start': start, 'end': end}
        if room:
            new_period['room'] = room
        
        self.timetable[day]['periods'].append(new_period)
        self.timetable[day]['periods'].sort(key=lambda x: x['start'])
        
        self.period_name_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)
        self.room_entry.delete(0, tk.END)
        
        self.update_template_list()
        messagebox.showinfo("Success", f"Period added to {day}!")
    
    def remove_period(self):
        selection = self.periods_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a period to remove!")
            return
        
        day = self.day_var.get()
        index = selection[0]
        
        if day in self.timetable and index < len(self.timetable[day]['periods']):
            removed = self.timetable[day]['periods'].pop(index)
            self.update_template_list()
            messagebox.showinfo("Success", f"Removed: {removed['name']}")
    
    def update_template_list(self):
        self.periods_listbox.delete(0, tk.END)
        day = self.day_var.get()
        
        if day in self.timetable:
            for period in self.timetable[day]['periods']:
                start_str = period['start'].strftime('%H:%M')
                end_str = period['end'].strftime('%H:%M')
                room_str = f" - {period['room']}" if 'room' in period else ""
                self.periods_listbox.insert(tk.END, f"{period['name']} ({start_str}-{end_str}){room_str}")
    
    def create_new_timetable(self):
        filename = filedialog.asksaveasfilename(
            title="Create new timetable",
            defaultextension=".json",
            filetypes=[('JSON files', '*.json'), ('XML files', '*.xml')]
        )
        
        if filename:
            empty_timetable = {
                'Monday': {'periods': []},
                'Tuesday': {'periods': []},
                'Wednesday': {'periods': []},
                'Thursday': {'periods': []},
                'Friday': {'periods': []}
            }
            
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as file:
                        json.dump(empty_timetable, file, indent=4)
                elif filename.endswith('.xml'):
                    root = ET.Element("timetable")
                    for day_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                        day_elem = ET.SubElement(root, "day", name=day_name)
                    tree = ET.ElementTree(root)
                    tree.write(filename, encoding='utf-8', xml_declaration=True)
                
                self.timetable = empty_timetable
                self.current_timetable_file = filename
                self.save_config()
                self.update_template_list()
                messagebox.showinfo("Success", f"New timetable created at {filename}")
                self.update_status_label(f"Editing: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create timetable: {str(e)}")
    
    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="🏫 School Day Timers 🏫",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=20)
        
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        upload_button = tk.Button(
            button_frame,
            text="📂 Upload Timetable",
            command=self.upload_timetable,
            bg=self.accent_color,
            fg=self.fg_color,
            font=("Helvetica", 10, "bold"),
            padx=10
        )
        upload_button.pack(side=tk.LEFT, padx=5)
        
        new_button = tk.Button(
            button_frame,
            text="🆕 New Timetable",
            command=self.create_new_timetable,
            bg=self.period_color,
            fg=self.fg_color,
            font=("Helvetica", 10, "bold"),
            padx=10
        )
        new_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(
            self.root,
            text=f"Loaded: {os.path.basename(self.current_timetable_file) if self.current_timetable_file else 'Default Timetable'}",
            font=("Helvetica", 9),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.status_label.pack(pady=5)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        timer_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(timer_frame, text="Timers")
        
        template_frame = tk.Frame(notebook, bg=self.template_bg)
        notebook.add(template_frame, text="Template Editor")
        
        self.current_time_label = tk.Label(
            timer_frame,
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.current_time_label.pack(pady=10)
        
        self.create_timer_frame(timer_frame, "📅 End of School Day (3:20 PM)", "school_end", self.weekend_color)
        self.create_timer_frame(timer_frame, "🎉 End of Week (Friday 3:20 PM)", "week_end", self.weekend_color)
        self.create_timer_frame(timer_frame, "⏰ Next Period Transition", "next_period", self.weekend_color)
        
        self.current_period_frame = tk.Frame(timer_frame, bg=self.bg_color)
        self.current_period_frame.pack(pady=20, fill=tk.X, padx=20)
        
        self.current_period_label = tk.Label(
            self.current_period_frame,
            text="Current Period: --",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.current_period_label.pack()
        
        self.current_room_label = tk.Label(
            self.current_period_frame,
            text="Room: --",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.current_room_label.pack()
        
        next_period_frame = tk.Frame(timer_frame, bg=self.bg_color)
        next_period_frame.pack(pady=5, fill=tk.X, padx=20)
        
        self.next_period_name_label = tk.Label(
            next_period_frame,
            text="Next Period: --",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.next_period_name_label.pack()
        
        self.next_period_room_label = tk.Label(
            next_period_frame,
            text="Room: --",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.next_period_room_label.pack()
        
        template_title = tk.Label(
            template_frame,
            text="📝 Timetable Template Editor",
            font=("Helvetica", 16, "bold"),
            bg=self.template_bg,
            fg=self.fg_color
        )
        template_title.pack(pady=10)
        
        day_frame = tk.Frame(template_frame, bg=self.template_bg)
        day_frame.pack(pady=10)
        
        tk.Label(day_frame, text="Select Day:", bg=self.template_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        self.day_var = tk.StringVar(value="Monday")
        day_menu = ttk.Combobox(day_frame, textvariable=self.day_var, values=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], state='readonly')
        day_menu.pack(side=tk.LEFT, padx=5)
        day_menu.bind('<<ComboboxSelected>>', lambda e: self.update_template_list())
        
        input_frame = tk.Frame(template_frame, bg=self.template_bg)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Period Name:", bg=self.template_bg, fg=self.fg_color).grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.period_name_entry = tk.Entry(input_frame, width=20)
        self.period_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Start (HH:MM):", bg=self.template_bg, fg=self.fg_color).grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.start_time_entry = tk.Entry(input_frame, width=20)
        self.start_time_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="End (HH:MM):", bg=self.template_bg, fg=self.fg_color).grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.end_time_entry = tk.Entry(input_frame, width=20)
        self.end_time_entry.grid(row=2, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Room (optional):", bg=self.template_bg, fg=self.fg_color).grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.room_entry = tk.Entry(input_frame, width=20)
        self.room_entry.grid(row=3, column=1, padx=5, pady=2)
        
        button_frame2 = tk.Frame(template_frame, bg=self.template_bg)
        button_frame2.pack(pady=10)
        
        tk.Button(button_frame2, text="➕ Add Period", command=self.save_template, bg=self.accent_color, fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame2, text="❌ Remove Selected", command=self.remove_period, bg=self.period_color, fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        
        list_frame = tk.Frame(template_frame, bg=self.template_bg)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(list_frame, text="Current Periods:", bg=self.template_bg, fg=self.fg_color).pack(anchor='w')
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.periods_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
        self.periods_listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.periods_listbox.yview)
        
        self.update_template_list()
    
    def update_status_label(self, text):
        self.status_label.config(text=text)
    
    def create_timer_frame(self, parent, title, timer_name, color):
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(pady=10, fill=tk.X, padx=20)
        
        label = tk.Label(
            frame,
            text=title,
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            fg=color
        )
        label.pack()
        
        timer_label = tk.Label(
            frame,
            text="--:--:--",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        timer_label.pack()
        
        setattr(self, f"{timer_name}_timer", timer_label)
    
    def get_current_period(self, current_datetime):
        current_day = current_datetime.strftime("%A")
        current_time = current_datetime.time()
        
        if current_day in self.timetable:
            periods = self.timetable[current_day]['periods']
            
            for period in periods:
                if period['start'] <= current_time <= period['end']:
                    return period
        
        return None
    
    def get_next_period(self, current_datetime):
        current_day = current_datetime.strftime("%A")
        current_time = current_datetime.time()
        
        if current_day in self.timetable:
            periods = self.timetable[current_day]['periods']
            
            for i, period in enumerate(periods):
                if current_time < period['start']:
                    return period
                elif period['start'] <= current_time <= period['end']:
                    if i + 1 < len(periods):
                        return periods[i + 1]
                    else:
                        next_day = self.get_next_school_day(current_day)
                        return self.timetable[next_day]['periods'][0]
        
        next_day = self.get_next_school_day(current_day)
        return self.timetable[next_day]['periods'][0]
    
    def get_next_school_day(self, current_day):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days.index(current_day)
        
        for i in range(1, 8):
            next_index = (current_index + i) % 7
            next_day = days[next_index]
            if next_day in self.timetable:
                return next_day
        
        return 'Monday'
    
    def format_time_remaining(self, seconds):
        if seconds < 0:
            return "00:00:00"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def calculate_school_end_time(self, current_datetime):
        end_time = datetime.combine(
            current_datetime.date(),
            time(15, 20)
        )
        
        if current_datetime > end_time:
            end_time = datetime.combine(
                current_datetime.date() + timedelta(days=1),
                time(15, 20)
            )
        
        return int((end_time - current_datetime).total_seconds())
    
    def calculate_week_end_time(self, current_datetime):
        days_until_friday = (4 - current_datetime.weekday()) % 7
        
        if days_until_friday == 0 and current_datetime.time() > time(15, 20):
            days_until_friday = 7
        
        friday_date = current_datetime.date() + timedelta(days=days_until_friday)
        friday_end = datetime.combine(friday_date, time(15, 20))
        
        return int((friday_end - current_datetime).total_seconds())
    
    def calculate_next_period_time(self, current_datetime):
        current_day = current_datetime.strftime("%A")
        current_time = current_datetime.time()
        
        if current_day in self.timetable:
            periods = self.timetable[current_day]['periods']
            
            for period in periods:
                if current_time < period['start']:
                    next_start = datetime.combine(
                        current_datetime.date(),
                        period['start']
                    )
                    return int((next_start - current_datetime).total_seconds())
                
                elif period['start'] <= current_time <= period['end']:
                    next_end = datetime.combine(
                        current_datetime.date(),
                        period['end']
                    )
                    return int((next_end - current_datetime).total_seconds())
        
        next_day = self.get_next_school_day(current_day)
        days_ahead = (list(self.timetable.keys()).index(next_day) - current_datetime.weekday()) % 7
        next_date = current_datetime.date() + timedelta(days=days_ahead)
        next_start = datetime.combine(next_date, time(8, 45))
        return int((next_start - current_datetime).total_seconds())
    
    def update_timers(self):
        current_datetime = datetime.now()
        
        self.current_time_label.config(
            text=current_datetime.strftime("%A, %B %d, %Y %I:%M:%S %p")
        )
        
        school_seconds = self.calculate_school_end_time(current_datetime)
        self.school_end_timer.config(
            text=self.format_time_remaining(school_seconds)
        )
        
        week_seconds = self.calculate_week_end_time(current_datetime)
        self.week_end_timer.config(
            text=self.format_time_remaining(week_seconds)
        )
        
        next_period_seconds = self.calculate_next_period_time(current_datetime)
        self.next_period_timer.config(
            text=self.format_time_remaining(next_period_seconds)
        )
        
        current_period = self.get_current_period(current_datetime)
        next_period = self.get_next_period(current_datetime)
        
        if current_period:
            self.current_period_label.config(
                text=f"Current: {current_period['name']}"
            )
            
            if 'room' in current_period:
                self.current_room_label.config(
                    text=f"Room: {current_period['room']}"
                )
            else:
                self.current_room_label.config(text="")
        else:
            self.current_period_label.config(text="Current: --")
            self.current_room_label.config(text="")
        
        if next_period:
            self.next_period_name_label.config(
                text=f"Next Period: {next_period['name']}"
            )
            
            if 'room' in next_period:
                self.next_period_room_label.config(
                    text=f"Room: {next_period['room']}"
                )
            else:
                self.next_period_room_label.config(text="")
        
        if school_seconds == 60:
            self.send_notification("School Day", "School ends in 1 minute!")
        elif school_seconds == 0:
            self.send_notification("School Day", "School has ended!")
        
        self.root.after(1000, self.update_timers)
    
    def send_notification(self, title, message):
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=5
            )
        except:
            pass

def main():
    root = tk.Tk()
    app = SchoolDayTimer(root)
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_closing():
        app.save_config()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
