import random
import tkinter as tk
from tkinter import messagebox
import json
import os

class ComTam6NightsGame:
    BG = "#0f1115"
    PANEL = "#181c22"
    PANEL2 = "#20252d"
    BORDER = "#353c47"
    TEXT = "#f1f5f9"
    MUTED = "#aab4c3"
    GOLD = "#ffcc66"
    GREEN = "#4ade80"
    RED = "#ef6461"
    CYAN = "#5eead4"

    def __init__(self, root):
        self.root = root
        self.root.title("ComTam6NightsGame ")
        self.root.configure(bg=self.BG)
        self.root.minsize(980, 760)
        self.center_window(1100, 800)

        self.default_font = ("Segoe UI", 10)
        self.bold_font = ("Segoe UI", 10, "bold")
        self.title_font = ("Segoe UI", 28, "bold")
        self.big_font = ("Segoe UI", 15, "bold")

        self.clue_database = [
            "Bức ảnh giao dịch mờ ám ở bến cảng",
            "Cuốn sổ nợ đen có chữ ký tay sai",
            "Băng ghi âm lệnh tống tiền của Kiều Lương Tâm",
            "Sơ đồ thiết kế nhà kho ngoại ô",
            "Chìa khóa rỉ sét mở cửa hầm bí mật",
            "Mật mã liên lạc bộ đàm đêm cuối",
            "Danh sách quan chức bị tha hóa nhận hối lộ",
            "Bản đồ tuyến đường vận chuyển nội tạng ngầm",
            "Dữ liệu camera ẩn trong phòng thu tiền",
            "Mẫu DNA chứng minh tội phạm trực tiếp"
        ]

        self.deduction_rules = [
            ("Bức ảnh giao dịch mờ ám ở bến cảng", "Cuốn sổ nợ đen có chữ ký tay sai", "Xác định rõ danh tính tay sai chủ chốt", 80, -10),
            ("Băng ghi âm lệnh tống tiền của Kiều Lương Tâm", "Mật mã liên lạc bộ đàm đêm cuối", "Giải mã tần số liên lạc ngầm của trùm", 100, -12),
            ("Sơ đồ thiết kế nhà kho ngoại ô", "Bản đồ tuyến đường vận chuyển nội tạng ngầm", "Khóa chặt vị trí sào huyệt và tuyến vận chuyển", 120, -15),
            ("Chìa khóa rỉ sét mở cửa hầm bí mật", "Dữ liệu camera ẩn trong phòng thu tiền", "Xác định hầm chứa quỹ đen của tổ chức", 150, -18),
            ("Danh sách quan chức bị tha hóa nhận hối lộ", "Mẫu DNA chứng minh tội phạm trực tiếp", "Hoàn thiện hồ sơ đại án đủ sức vây bắt", 200, -20)
        ]

        self.achievement_database = {
            "Ach_1": ("Bậc Thầy Trinh Sát", "Bắt gọn trùm Kiều Lương Tâm (True Ending 6)."),
            "Ach_2": ("Vua Cơm Tấm", "Nâng cấp Nước Mắm Bí Truyền lên cấp tối đa (Cấp 3)."),
            "Ach_3": ("Thám Tử Học Thức", "Thực hiện thành công ít nhất 3 lượt suy luận trên Sơ Đồ Tư Duy."),
            "Ach_4": ("Mình Đồng Da Sắt", "Trải qua 6 đêm mà không bao giờ mua Áo Giáp Chống Đạn."),
            "Ach_5": ("Đại Gia Phố Cổ", "Tích lũy số vốn đạt từ $1000 trở lên."),
            "Ach_6": ("Thần Thoại Endings", "Khám phá trọn vẹn toàn bộ 8/8 Kết cục của game.")
        }
        
        self.save_file = "comtam_6nights_endings.json"
        self.unlocked_endings = set()
        self.unlocked_achievements = set()
        self.load_endings()
        
        self.reset_game_data()
        self.build_main_menu()

    def load_endings(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.unlocked_endings = set(data.get("endings", []))
                    self.unlocked_achievements = set(data.get("achievements", []))
            except:
                self.unlocked_endings = set()
                self.unlocked_achievements = set()

    def save_endings(self):
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump({
                "endings": list(self.unlocked_endings),
                "achievements": list(self.unlocked_achievements)
            }, f, ensure_ascii=False, indent=4)

    def check_achievements(self):
        new_unlocked = []

        if "Ending 6" in self.unlocked_endings and "Ach_1" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_1")
            new_unlocked.append(self.achievement_database["Ach_1"][0])

        if self.recipe_level >= 3 and "Ach_2" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_2")
            new_unlocked.append(self.achievement_database["Ach_2"][0])

        if getattr(self, "deduction_count", 0) >= 3 and "Ach_3" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_3")
            new_unlocked.append(self.achievement_database["Ach_3"][0])

        if self.night >= 6 and not getattr(self, "bought_armor_ever", False) and "Ach_4" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_4")
            new_unlocked.append(self.achievement_database["Ach_4"][0])

        if self.money >= 1000 and "Ach_5" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_5")
            new_unlocked.append(self.achievement_database["Ach_5"][0])

        if len(self.unlocked_endings) >= 8 and "Ach_6" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_6")
            new_unlocked.append(self.achievement_database["Ach_6"][0])

        if new_unlocked:
            self.save_endings()
            for name in new_unlocked:
                messagebox.showinfo("🏆 THÀNH TỰU MỚI MỞ KHÓA!", f"Chúc mừng! Bạn đã đạt thành tựu danh giá:\n\n🏆 [{name}]", parent=self.root)

    def show_achievements(self):
        self.check_achievements()
        text = f"TỔNG SỐ THÀNH TỰU ĐÃ ĐẠT: {len(self.unlocked_achievements)}/6\n\n"
        for code, (title, desc) in self.achievement_database.items():
            status = "✅ ĐÃ ĐẠT" if code in self.unlocked_achievements else "🔒 Chưa mở"
            text += f"• {title} -> [{status}]\n  {desc}\n\n"
        messagebox.showinfo("Thành Tựu & Huy Hiệu Phá Án", text)

    def center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max((sw - width) // 2, 0)
        y = max((sh - height) // 2, 0)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def center_window_dialog(self, win, width, height):
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = max((sw - width) // 2, 0)
        y = max((sh - height) // 2, 0)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, width=20, bg=None, fg="white", height=1, state="normal"):
        return tk.Button(
            parent, text=text, command=command, width=width, height=height, state=state,
            font=self.bold_font, bg=bg or self.PANEL2, fg=fg,
            activebackground="#39414d", activeforeground="white",
            relief="flat", bd=0, cursor="hand2"
        )

    def get_weather_name(self):
        weathers = {
            1: "TRỜI TỊNH",
            2: "MƯA TẦM TÃ",
            3: "CÚP ĐIỆN",
            4: "GIÓ BÃO GIẬT",
            5: "THANH TRA ĐỘT XUẤT",
            6: "ĐÊM SINH TỬ"
        }
        return weathers.get(self.night, "Bình thường")

    def get_weather_description(self):
        descs = {
            1: "Đêm 1: Trời quang mây tịnh. Hoạt động bán hàng diễn ra bình thường.",
            2: "Đêm 2: Mưa tầm tã & Sương mù. Khách hàng cảnh giác hơn (+5% nghi ngờ khi làm lỗi).",
            3: "Đêm 3: Cúp điện chập chờn! Cần 'Bóng đèn công suất lớn' để tránh phạt gấp đôi nghi ngờ.",
            4: "Đêm 4: Gió bão giật mạnh! Khách hàng vội vã, dễ xảy ra sai sót.",
            5: "Đêm 5: Thanh tra đô thị kiểm tra diện rộng! Nghi ngờ tăng nhanh nếu sai sót.",
            6: "Đêm 6: Đêm quyết chiến cuối cùng! Thu thập đủ 10 manh mối để giăng bẫy toàn diện."
        }
        return descs.get(self.night, "")

    def reset_game_data(self):
        self.game_running = False
        self.money = 50
        self.suspicion = random.randint(15, 30)
        self.clues = 0
        self.max_clues = 10
        self.night = 1
        self.orders_completed_tonight = 0
        self.recipe_level = 0
        self.serve_reward = 45
        self.deduction_count = 0
        self.bought_armor_ever = False
        
        self.has_light = False
        self.has_armor = False
        self.has_air_filter = False
        self.has_camera = False
        self.has_special_knife = False
        self.has_compartment_upgrade = False
        self.has_speaker = False
        self.has_jammer = False
        self.has_fake_docs = False
        self.has_magnifier = False
        
        self.has_wooden_tables = False
        self.has_ceiling_fan = False
        self.has_iron_door = False
        
        self.has_meo_chieu_tai = False
        self.has_bien_hieu_vip = False
        self.is_vip_customer = False

        self.has_sedative = False
        self.has_vip_license = False
        self.has_radio_scanner = False
        self.has_fake_tape = False
        self.has_radio_detector = False
        
        self.police_compromised = False 
        self.informant_active = False
        
        self.talked_current_customer = False
        self.hidden_compartment = []
        self.max_compartment = 2
        self.is_smuggler_customer = False
        
        self.collected_clue_names = []
        self.completed_deductions = set()
        
        self.current_customer = None
        self.current_plate = []
        self.customer_visual = None
        self.in_arrest_mode = False
        self.arrest_step = 0
        self.hour = 20
        self.minute = 0

    def add_clue(self):
        if self.clues < len(self.clue_database):
            new_clue = self.clue_database[self.clues]
            self.collected_clue_names.append(new_clue)
            self.clues += 1
            return new_clue
        return None

    def build_main_menu(self):
        self.clear_root()
        self.game_running = False
        self.in_arrest_mode = False

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=40, pady=25)

        top = tk.Frame(outer, bg=self.BG)
        top.pack(fill="both", expand=True)

        tk.Label(top, text="ComTam6NightsGame", font=("Segoe UI", 32, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(10, 2))
        tk.Label(top, text="CREATOR BY: Q-HOUSETEAM", font=("Segoe UI", 12, "bold"), fg=self.CYAN, bg=self.BG).pack(pady=(0, 10))
        tk.Label(
            top, text="Phiên bản v1.1.0: Trang Bị Nâng Cấp Quán, Thành Tựu & Huy Hiệu, Sơ Đồ Tư Duy.",
            font=("Segoe UI", 10), fg=self.MUTED, bg=self.BG, justify="center"
        ).pack(pady=(0, 10))

        card = tk.Frame(top, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(ipadx=30, ipady=10)

        tk.Label(card, text="TÍNH NĂNG MỚI BẢN v1.1.0", font=("Segoe UI", 12, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(0, 6))
        tk.Label(
            card,
            text="• Nâng Cấp Nội Thất Quán: Bàn Ghế Gỗ Sưa, Quạt Trần Công Nghiệp & Cửa Sắt Cuốn Cường Lực.\n"
                 "• Hệ Thống Thành Tựu & Huy Hiệu: Mở khóa 6 danh hiệu trinh sát cao quý.\n"
                 "• Sơ Đồ Tư Duy (Mind Map Deduction): Ghép nối manh mối thu thập được để giải mã câu đố.\n"
                 "• NPC Cốt Truyện Chi Tiết: Bà Cụ Bán Nước Mía, Cậu Bé Đánh Giày, Thiếu Úy Nam, Lĩnh 'Đen'...\n"
                 "• Đa kết cục phong phú (8 Endings): Khám phá các Ending ẩn tùy thuộc Tiền & Nghi ngờ.",
            font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL, justify="left"
        ).pack()

        buttons = tk.Frame(outer, bg=self.BG)
        buttons.pack(pady=10)

        self.make_button(buttons, "BẮT ĐẦU CHUYÊN ÁN", self.start_game, width=28, height=2, bg="#167c63").pack(pady=3)
        self.make_button(buttons, f"THƯ VIỆN ENDING ({len(self.unlocked_endings)}/8)", self.show_endings, width=28, height=2, bg="#2b6cb0").pack(pady=3)
        self.make_button(buttons, f"THÀNH TỰU & HUY HIỆU ({len(self.unlocked_achievements)}/6)", self.show_achievements, width=28, height=2, bg="#d97706").pack(pady=3)
        self.make_button(buttons, "ĐÊM 0 - HUẤN LUYỆN", self.start_night_0_tutorial, width=28, height=2, bg="#3b4654").pack(pady=3)
        self.make_button(buttons, "THOÁT GAME", self.root.destroy, width=28, height=2, bg="#9c3d3d").pack(pady=3)

    def show_endings(self):
        end_names = [
            "Ending 1: Thân phận bị lật tẩy (GameOver)",
            "Ending 2: Ôm tiền trốn ra nước ngoài (Ẩn)",
            "Ending 3: Vua Cơm Tấm hoàn lương (Ẩn)",
            "Ending 4: Bị sát thủ thủ tiêu (Bad End)",
            "Ending 5: Sập bẫy do do dự phút cuối",
            "Ending 6: Bắt gọn Kiều Lương Tâm (True End)",
            "Ending 7: Sập bẫy Cảnh sát bị chiếm quyền",
            "Ending 8: Thất bại do thiếu manh mối (Normal)"
        ]
        statuses = ["ĐÃ MỞ KHÓA" if f"Ending {i}" in self.unlocked_endings else "🔒 Chưa khám phá" for i in range(1, 9)]
        
        text = f"TỔNG SỐ ENDING ĐÃ KHÁM PHÁ: {len(self.unlocked_endings)}/8\n\n"
        for i in range(8):
            text += f"{end_names[i]} -> [{statuses[i]}]\n"

        messagebox.showinfo("Endings", text)

    def start_night_0_tutorial(self):
        lessons = [
            ("Bài 1: Quy trình Phục vụ & Làm đĩa cơm",
             "• Xem YÊU CẦU MÓN của khách trên giao diện.\n"
             "• Nhấn các nút nguyên liệu (Cơm, Sườn, Trứng, Chả, Bì) để làm đúng đĩa cơm.\n"
             "• Nhấn 'PHỤC VỤ MÓN': Phục vụ đúng nhận tiền + giảm nghi ngờ. Phục vụ sai bị phạt tiền và tăng độ nghi ngờ!"),
            
            ("Bài 2: Quản lý Độ Nghi Ngờ & Thời Tiết",
             "• Độ Nghi Ngờ chạm 100% = Thân phận cảnh sát chìm bị lật tẩy (GAME OVER)!\n"
             "• Mỗi đêm có thời tiết khác nhau (Mưa, Cúp điện, Thanh tra...).\n"
             "• Mua vật phẩm bổ trợ ở Cửa Hàng Đêm Muộn để giảm rủi ro thời tiết."),
            
            ("Bài 3: Gói Hàng Ngầm & Khoang Bí Mật",
             "• Khách hàng băng nhóm có thể đem GÓI HÀNG NGẦM đến nhờ cất giấu.\n"
             "• Nhấn 'NHẬN GÓI HÀNG NGẦM' để cất vào khoang bí mật dưới gầm bàn và lấy tiền công.\n"
             "• Cẩn thận: Nếu khoang bí mật bị đầy mà vẫn nhận hàng, gói hàng sẽ rơi ra ngoài khiến Độ nghi ngờ +40%!"),

            ("Bài 4: Khách VIP, Nước Mắm Bí Truyền & Trang Bị Quán",
             "• Nâng cấp Nước Mắm Bí Truyền qua 3 cấp ($150->$65, $200->$70, $300->$90) để tăng thu nhập mỗi suất.\n"
             "• Mua Bàn Ghế Gỗ Sưa, Quạt Trần Công Nghiệp & Cửa Sắt Cuốn Cường Lực để tăng doanh thu và an toàn."),

            ("Bài 5: Sơ Đồ Tư Duy & Thành Tựu Huy Hiệu",
             "• Mở 'SƠ ĐỒ TƯ DUY' trong ca trực để ghép nối các manh mối với nhau, nhận thưởng tiền & giảm Độ nghi ngờ.\n"
             "• Mở khóa 6 Thành Tựu Huy Hiệu danh giá tại Menu chính."),

            ("Bài 6: Thu Thập 10 Manh Mối & Đêm 6 Quyết Chiến",
             "• Thực hiện Nhiệm vụ Ban Ngày và Điều tra để thu thập đủ 10 Manh Mối.\n"
             "• Đêm 6: Bấm 'GIĂNG BẪY' để vây bắt ông trùm Kiều Lương Tâm.\n"
             "• Game có 8 Kết cục phong phú dựa trên Tiền và Độ nghi ngờ!")
        ]

        tut_win = tk.Toplevel(self.root)
        tut_win.title("ĐÊM 0 - HUẤN LUYỆN TOÀN DIỆN GAMEPLAY")
        tut_win.configure(bg=self.PANEL)
        tut_win.transient(self.root)
        tut_win.grab_set()
        self.center_window_dialog(tut_win, 620, 380)

        current_idx = [0]

        lbl_title = tk.Label(tut_win, text="", font=("Segoe UI", 13, "bold"), fg=self.GOLD, bg=self.PANEL)
        lbl_title.pack(pady=(15, 8))

        card = tk.Frame(tut_win, bg=self.PANEL2, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=5)

        lbl_content = tk.Label(card, text="", font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL2, justify="left", wraplength=540)
        lbl_content.pack(padx=15, pady=15, anchor="w")

        lbl_step = tk.Label(tut_win, text="", font=("Segoe UI", 9, "italic"), fg=self.CYAN, bg=self.PANEL)
        lbl_step.pack(pady=2)

        btn_frame = tk.Frame(tut_win, bg=self.PANEL)
        btn_frame.pack(fill="x", pady=10, padx=20)

        def update_lesson():
            idx = current_idx[0]
            title, content = lessons[idx]
            lbl_title.config(text=f"🎓 ĐÊM 0: HUẤN LUYỆN - {title}")
            lbl_content.config(text=content)
            lbl_step.config(text=f"Bài học {idx + 1} / 6")

            btn_prev.config(state="normal" if idx > 0 else "disabled")
            if idx == len(lessons) - 1:
                btn_next.config(text="HOÀN THÀNH (VỀ MENU)", bg="#167c63")
            else:
                btn_next.config(text="BÀI TIẾP THEO ->", bg="#2b6cb0")

        def next_lesson():
            if current_idx[0] < len(lessons) - 1:
                current_idx[0] += 1
                update_lesson()
            else:
                tut_win.destroy()
                messagebox.showinfo("Huấn luyện hoàn tất", "Bạn đã hoàn thành Đêm 0 Huấn Luyện! Sẵn sàng bước vào chuyên án chính thức.", parent=self.root)

        def prev_lesson():
            if current_idx[0] > 0:
                current_idx[0] -= 1
                update_lesson()

        btn_prev = self.make_button(btn_frame, "<- BÀI TRƯỚC", prev_lesson, width=15, bg="#3b4654")
        btn_prev.pack(side="left")

        btn_next = self.make_button(btn_frame, "BÀI TIẾP THEO ->", next_lesson, width=22, bg="#2b6cb0")
        btn_next.pack(side="right")

        update_lesson()

    def start_game(self):
        self.reset_game_data()
        self.game_running = True
        self.build_game_ui()

        intro_text = (
            "Sương mù bao trùm con hẻm nhỏ. Dưới lớp tạp dề, bạn đảm nhận chiến dịch 6 đêm "
            "triệt phá đường dây tội phạm của Kiều Lương Tâm.\n\n"
            "TÍNH NĂNG MỚI : Trang bị Quán Cơm, SƠ ĐỒ TƯ DUY và hệ thống THÀNH TỰU HUY HIỆU đã sẵn sàng!"
        )
        messagebox.showinfo("Lời khởi đầu", intro_text)
        self.next_customer()

    def build_game_ui(self):
        self.clear_root()

        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=18, pady=12)

        header = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        header.pack(fill="x", pady=(0, 8))

        top_row = tk.Frame(header, bg=self.PANEL)
        top_row.pack(fill="x", padx=15, pady=(8, 2))

        self.lbl_title = tk.Label(top_row, text="ComTam6NightsGame(Q-HouseTeam)", font=("Segoe UI", 14, "bold"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_title.pack(side="left")

        self.lbl_stats = tk.Label(top_row, text="", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL)
        self.lbl_stats.pack(side="right")

        self.lbl_weather_info = tk.Label(header, text="", font=("Segoe UI", 9, "italic"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_weather_info.pack(anchor="w", padx=15, pady=(0, 8))

        scene_box = tk.Frame(main, bg="#111318", highlightbackground=self.BORDER, highlightthickness=1)
        scene_box.pack(fill="x", pady=(0, 6))

        self.canvas_view = tk.Canvas(scene_box, height=160, bg="#111318", highlightthickness=0, bd=0)
        self.canvas_view.pack(fill="x", padx=8, pady=6)

        self.lbl_canvas_status = tk.Label(scene_box, text="Đang chờ khách...", font=("Segoe UI", 11, "bold"), fg=self.GOLD, bg="#111318")
        self.lbl_canvas_status.pack(pady=(0, 8))

        dialog_box = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        dialog_box.pack(fill="x", pady=4)

        tk.Label(dialog_box, text="DIỄN BIẾN CHUYÊN ÁN & TIN BÁO TÌNH BÁO", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL).pack(anchor="w", padx=12, pady=(6, 2))
        self.lbl_dialog = tk.Label(dialog_box, text="", font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL, wraplength=1000, justify="left", anchor="w")
        self.lbl_dialog.pack(fill="x", padx=12, pady=(0, 8))

        self.kitchen_frame = tk.LabelFrame(
            main, text=" GÓC BẾP & KHOANG BÍ MẬT DƯỚI GẦM BÀN ", font=("Segoe UI", 10, "bold"),
            fg=self.GOLD, bg=self.PANEL2, padx=10, pady=8,
            highlightbackground=self.BORDER, highlightthickness=1, bd=0
        )
        self.kitchen_frame.pack(fill="x", pady=4)

        plate_row = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        plate_row.pack(fill="x", pady=(0, 4))

        self.lbl_plate = tk.Label(plate_row, text="Đĩa cơm đang làm: [Trống]", font=("Segoe UI", 10, "bold"), fg="#ffb454", bg=self.PANEL2)
        self.lbl_plate.pack(side="left")

        self.lbl_compartment = tk.Label(plate_row, text=f"Khoang ngầm: [0/{self.max_compartment}]", font=("Segoe UI", 10, "bold"), fg=self.RED, bg=self.PANEL2)
        self.lbl_compartment.pack(side="right")

        self.ing_frame = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        self.ing_frame.pack(fill="x", pady=(4, 0))

        for text, value in [("Cơm", "Cơm"), ("Sườn", "Sườn"), ("Trứng", "Trứng"), ("Chả", "Chả"), ("Bì", "Bì")]:
            btn = self.make_button(self.ing_frame, text, lambda item=value: self.add_ing(item), width=9)
            btn.pack(side="left", padx=2)

        self.btn_reset_plate = self.make_button(self.ing_frame, "LÀM LẠI", self.reset_plate, width=9, bg="#9c3d3d")
        self.btn_reset_plate.pack(side="left", padx=(10, 2))

        self.btn_serve = self.make_button(self.ing_frame, "PHỤC VỤ MÓN", self.serve_plate, width=14, bg="#248f57")
        self.btn_serve.pack(side="right", padx=2)

        actions = tk.Frame(main, bg=self.BG)
        actions.pack(fill="x", pady=(6, 0))

        self.btn_talk = self.make_button(actions, "ĐỐI THOẠI", self.action_talk_customer, width=15, bg="#2b6cb0", height=2)
        self.btn_talk.pack(side="left", expand=True, fill="x", padx=(0, 2))

        self.btn_investigate = self.make_button(actions, "ĐIỀU TRA", self.action_investigate, width=15, bg="#384454", height=2)
        self.btn_investigate.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_mindmap = self.make_button(actions, "SƠ ĐỒ TƯ DUY", self.open_mindmap_ui, width=16, bg="#d97706", height=2)
        self.btn_mindmap.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_smuggled_action = self.make_button(actions, "NHẬN HÀNG NGẦM", self.action_take_smuggled_package, width=16, bg="#805ad5", height=2, state="disabled")
        self.btn_smuggled_action.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_arrest = self.make_button(actions, "GIĂNG BẪY", self.action_arrest, width=16, bg="#a63c3c", height=2)
        self.btn_arrest.pack(side="left", expand=True, fill="x", padx=(2, 0))

        bottom = tk.Frame(main, bg=self.BG)
        bottom.pack(fill="x", pady=(6, 0))
        self.make_button(bottom, "VỀ MENU", self.confirm_back_menu, width=14, bg="#303743").pack(side="left")

        self.update_stats()
        self.root.after(50, self.draw_counter_scene)

    def open_mindmap_ui(self):
        mm_win = tk.Toplevel(self.root)
        mm_win.title("SƠ ĐỒ TƯ DUY & SUY LUẬN BẰNG CHỨNG")
        mm_win.configure(bg=self.PANEL)
        mm_win.transient(self.root)
        mm_win.grab_set()
        self.center_window_dialog(mm_win, 780, 520)

        tk.Label(mm_win, text="🧠 SƠ ĐỒ TƯ DUY CHUYÊN ÁN (MIND MAP DEDUCTION)", font=("Segoe UI", 14, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(12, 4))
        tk.Label(mm_win, text="Ghép nối 2 manh mối tương ứng để đưa ra suy luận phá án quan trọng.", font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL).pack(pady=(0, 8))

        body = tk.Frame(mm_win, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=15, pady=5)

        left_frame = tk.LabelFrame(body, text=" MANH MỐI ĐÃ THU THẬP ", font=("Segoe UI", 9, "bold"), fg=self.CYAN, bg=self.PANEL2, bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        listbox_clues = tk.Listbox(left_frame, bg=self.BG, fg=self.TEXT, font=("Segoe UI", 9), selectmode="multiple", highlightthickness=0, bd=0)
        listbox_clues.pack(fill="both", expand=True, padx=8, pady=8)

        for c in self.collected_clue_names:
            listbox_clues.insert("end", f"• {c}")

        right_frame = tk.LabelFrame(body, text=" SƠ ĐỒ KẾT NỐI & SUY LUẬN ", font=("Segoe UI", 9, "bold"), fg=self.GOLD, bg=self.PANEL2, bd=1)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        canvas = tk.Canvas(right_frame, bg="#111318", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=8, pady=8)

        def draw_mindmap():
            canvas.delete("all")
            cw = canvas.winfo_width() or 360
            ch = canvas.winfo_height() or 320
            cx, cy = cw // 2, ch // 2

            canvas.create_oval(cx - 55, cy - 25, cx + 55, cy + 25, fill="#9c3d3d", outline=self.GOLD, width=2)
            canvas.create_text(cx, cy, text="KIỀU LƯƠNG TÂM\n(MỤC TIÊU)", fill="white", font=("Segoe UI", 9, "bold"), justify="center")

            n = len(self.collected_clue_names)
            if n == 0:
                canvas.create_text(cx, cy + 60, text="Chưa có manh mối nào!", fill=self.MUTED, font=("Segoe UI", 9, "italic"))
                return

            import math
            radius = min(cw, ch) // 2 - 40
            for i, clue_name in enumerate(self.collected_clue_names):
                angle = (2 * math.pi / max(n, 1)) * i
                nx = cx + int(radius * math.cos(angle))
                ny = cy + int(radius * math.sin(angle))

                canvas.create_line(cx, cy, nx, ny, fill="#353c47", width=1, dash=(3, 3))
                canvas.create_oval(nx - 18, ny - 18, nx + 18, ny + 18, fill="#2b6cb0", outline=self.CYAN, width=1)
                canvas.create_text(nx, ny, text=f"M{i+1}", fill="white", font=("Segoe UI", 9, "bold"))

        right_frame.after(100, draw_mindmap)

        btn_bar = tk.Frame(mm_win, bg=self.PANEL)
        btn_bar.pack(fill="x", pady=10, padx=15)

        def execute_deduction():
            selected_indices = listbox_clues.curselection()
            if len(selected_indices) != 2:
                messagebox.showwarning("Suy luận", "Vui lòng chọn đúng 2 manh mối từ danh sách để thực hiện ghép nối!", parent=mm_win)
                return

            c1 = self.collected_clue_names[selected_indices[0]]
            c2 = self.collected_clue_names[selected_indices[1]]

            found_rule = None
            for rule in self.deduction_rules:
                r1, r2, result_title, reward_m, susp_red = rule
                if (c1 == r1 and c2 == r2) or (c1 == r2 and c2 == r1):
                    found_rule = rule
                    break

            if found_rule:
                r1, r2, result_title, reward_m, susp_red = found_rule
                rule_key = f"{r1}|{r2}"
                if rule_key in self.completed_deductions:
                    messagebox.showinfo("Đã suy luận", "Bạn đã thực hiện ghép nối 2 manh mối này trước đó rồi!", parent=mm_win)
                    return

                self.completed_deductions.add(rule_key)
                self.money += reward_m
                self.suspicion = max(0, self.suspicion + susp_red)
                self.deduction_count += 1

                messagebox.showinfo(
                    "SUY LUẬN THÀNH CÔNG!",
                    f"💡 PHÁT HIỆN: {result_title}\n\n"
                    f"• Kinh phí thưởng: +${reward_m}\n"
                    f"• Độ nghi ngờ giảm: {abs(susp_red)}%\n\n"
                    f"Tiến trình lập hồ sơ chuyên án đã tiến thêm một bước lớn!",
                    parent=mm_win
                )
                self.check_achievements()
                self.update_stats()
                mm_win.destroy()
            else:
                messagebox.showwarning("Ghép nối thất bại", "2 manh mối này chưa tạo thành liên kết hợp lý. Hãy thử ghép cặp khác!", parent=mm_win)

        self.make_button(btn_bar, "GHÉP NỐI SUY LUẬN", execute_deduction, width=22, bg="#248f57").pack(side="left", padx=5)
        self.make_button(btn_bar, "ĐÓNG", mm_win.destroy, width=14, bg="#3b4654").pack(side="right", padx=5)

    def trigger_informant_event(self):
        if self.informant_active or self.clues >= self.max_clues:
            return
        self.informant_active = True

        inf_win = tk.Toplevel(self.root)
        inf_win.title("SỰ KIỆN: KẺ CHỈ ĐIỂM BÍ ẨN (THE INFORMANT)")
        inf_win.configure(bg=self.PANEL)
        inf_win.transient(self.root)
        inf_win.grab_set()
        self.center_window_dialog(inf_win, 560, 340)

        words = ["MANH MOI", "BANG DANG", "ONG TRUM", "SAO HUYET", "GIAU TIEN", "TANG VAT", "GIAI MA", "SAT THU"]
        target_word = random.choice(words)
        letters = list(target_word)
        random.shuffle(letters)
        scrambled = " ".join(letters)

        time_limit = 45 if getattr(self, "has_magnifier", False) else 30
        self.informant_time_left = time_limit

        tk.Label(inf_win, text="🕵️ KẺ CHỈ ĐIỂM XUẤT HIỆN!", font=("Segoe UI", 14, "bold"), fg=self.RED, bg=self.PANEL).pack(pady=(15, 5))
        tk.Label(inf_win, text="Một vị khách bí ẩn lén để lại mảnh giấy chứa mật mã rồi biến mất!\nGiải mã chuỗi ký tự đảo ngược trước khi tờ giấy tự hủy.", font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL, justify="center").pack(pady=(0, 10))

        lbl_scrambled = tk.Label(inf_win, text=f"MÃ HÓA:  {scrambled}", font=("Segoe UI", 16, "bold"), fg=self.GOLD, bg=self.PANEL2, relief="solid", bd=1, padx=15, pady=8)
        lbl_scrambled.pack(pady=5)

        lbl_timer = tk.Label(inf_win, text=f"⏱️ Thời gian còn lại: {self.informant_time_left} giây", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL)
        lbl_timer.pack(pady=5)

        entry_var = tk.StringVar()
        entry = tk.Entry(inf_win, textvariable=entry_var, font=("Segoe UI", 12, "bold"), justify="center", bg=self.BG, fg=self.TEXT, insertbackground="white")
        entry.pack(pady=8, ipadx=10, ipady=3)
        entry.focus()

        def update_timer():
            if not hasattr(self, "informant_time_left") or not inf_win.winfo_exists():
                return
            self.informant_time_left -= 1
            if self.informant_time_left <= 0:
                inf_win.destroy()
                self.informant_active = False
                messagebox.showwarning("Hết giờ!", "Mảnh giấy đã bị tiêu hủy! Bạn bỏ lỡ cơ hội nhận Manh mối quý giá.", parent=self.root)
            else:
                lbl_timer.config(text=f"⏱️ Thời gian còn lại: {self.informant_time_left} giây")
                inf_win.after(1000, update_timer)

        def submit_answer(event=None):
            ans = entry_var.get().strip().upper()
            if ans.replace(" ", "") == target_word.replace(" ", ""):
                inf_win.destroy()
                self.informant_active = False
                new_clue = self.add_clue()
                msg = f"Giải mã thành công!\nThu được vật chứng quý giá:\n+ {new_clue}\n(Tiến độ: {self.clues}/{self.max_clues})" if new_clue else "Giải mã thành công!"
                messagebox.showinfo("Thành công", msg, parent=self.root)
                self.update_stats()
            else:
                messagebox.showerror("Mật mã sai", "Mật mã chưa chính xác! Hãy thử lại nhanh lên.", parent=inf_win)
                entry_var.set("")

        entry.bind("<Return>", submit_answer)
        self.make_button(inf_win, "XÁC NHẬN GIẢI MÃ", submit_answer, width=20, bg="#248f57").pack(pady=8)
        inf_win.after(1000, update_timer)

    def build_shop_ui(self):
        self.clear_root()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(outer, text="CỬA HÀNG ĐÊM MUỘN", font=("Segoe UI", 22, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(5, 2))
        tk.Label(outer, text=f"CREATOR BY: Q-HOUSETEAM | Chuẩn bị trước Đêm {self.night} | Vốn: ${self.money}", font=("Segoe UI", 10), fg=self.CYAN, bg=self.BG).pack(pady=(0, 15))

        shop_card = tk.Frame(outer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        shop_card.pack(fill="both", expand=True, ipadx=10, ipady=5)

        recipe_name = "Nước Mắm Bí Truyền I"
        recipe_desc = "Tăng giá bán đĩa cơm từ $45 lên $65."
        recipe_cost = 150
        recipe_state = "normal"
        recipe_text = "MUA"

        if self.recipe_level == 1:
            recipe_name = "Nước Mắm Bí Truyền II"
            recipe_desc = "Tăng giá bán đĩa cơm từ $65 lên $70."
            recipe_cost = 200
        elif self.recipe_level == 2:
            recipe_name = "Nước Mắm Bí Truyền III"
            recipe_desc = "Tăng giá bán đĩa cơm từ $70 lên $90 (Tối đa)."
            recipe_cost = 300
        elif self.recipe_level >= 3:
            recipe_name = "Nước Mắm Bí Truyền (MAX)"
            recipe_desc = "Đã đạt cấp tối đa ($90/đĩa cơm)."
            recipe_cost = 0
            recipe_state = "disabled"
            recipe_text = "ĐÃ MUA TỐI ĐA"

        items = [
            ("Bộ Bàn Ghế Gỗ Sưa", "Tăng thêm 10% tỷ lệ Khách VIP và bo thêm $10 mỗi phần ăn.", 200, self.buy_wooden_tables, "has_wooden_tables"),
            ("Quạt Trần Công Nghiệp", "Mỗi lần phục vụ đúng món giúp giảm thêm 2% Độ nghi ngờ.", 160, self.buy_ceiling_fan, "has_ceiling_fan"),
            ("Cửa Sắt Cuốn Cường Lực", "Giảm 30% Độ nghi ngờ bị phạt khi chọn sai đối thoại hoặc tra hỏi.", 220, self.buy_iron_door, "has_iron_door"),
            ("Mèo Chiêu Tài", "Tăng 35% tỷ lệ Khách VIP (từ 10% -> 45%). Phục vụ đúng món bo thêm $25.", 220, self.buy_meo_chieu_tai, "has_meo_chieu_tai"),
            ("Biển Hiệu Cơm Tấm VIP", "Tăng thêm 15% tỷ lệ xuất hiện Khách VIP.", 180, self.buy_bien_hieu_vip, "has_bien_hieu_vip"),
            ("Dao Bếp Cao Cấp", "Làm đúng món bo thêm $25 thưởng kỹ năng làm bếp.", 160, self.buy_special_knife, "has_special_knife"),
            ("Loa Quảng Cáo Mini", "Tăng hiệu quả giảm độ nghi ngờ khi phục vụ đúng món.", 150, self.buy_speaker, "has_speaker"),
            ("Radio Rà Sóng Bộ Đàm", "Phát hiện trước nếu đêm nay Cảnh sát bị băng nhóm chiếm quyền (Bẫy ngược).", 250, self.buy_radio_detector, "has_radio_detector"),
            ("Kính Lúp Thám Tử", "Tăng thời gian giải mã Kẻ Chỉ Điểm lên 45s & Tỷ lệ Điều tra thành công lên 80%.", 280, self.buy_magnifier, "has_magnifier"),
            ("Áo giáp chống đạn", "Cứu mạng bạn 1 lần duy nhất khi Độ nghi ngờ chạm 100%.", 250, self.buy_armor, "has_armor"),
            ("Bóng đèn công suất lớn", "Khắc chế sự cố Cúp điện (Đêm 3) và giảm rủi ro thời tiết.", 120, self.buy_light, "has_light"),
            ("Máy lọc không khí ngầm", "Lọc sạch không khí sương mù, giảm ngay 15% Độ nghi ngờ.", 180, self.buy_air_filter, "has_air_filter"),
            ("Camera ngụy trang mini", "Tự động ghi hình hỗ trợ, giảm nhẹ hình phạt khi làm sai món.", 220, self.buy_camera, "has_camera"),
            ("Bộ dụng cụ mở rộng khoang", "Nâng cấp sức chứa Khoang bí mật từ 2 lên 4 gói hàng.", 180, self.buy_compartment_upgrade, "has_compartment_upgrade"),
            ("Thiết bị phá sóng mini", "Ngăn tín hiệu báo động. Không bị tăng nghi ngờ nếu lỡ từ chối nhận hàng ngầm.", 200, self.buy_jammer, "has_jammer"),
            ("Tài liệu ngụy tạo", "Qua mắt các trinh sát địch. Tự động giảm 10% Độ nghi ngờ ở đầu mỗi đêm.", 200, self.buy_fake_docs, "has_fake_docs"),
            ("Giấy phép kinh doanh VIP", "Khắc tinh của Thanh tra Đêm 5. Giảm 50% mọi hình phạt nghi ngờ khi làm sai món.", 350, self.buy_vip_license, "has_vip_license"),
            ("Máy quét vô tuyến tình báo", "Công nghệ cao cấp. Lập tức dò ra 1 Manh mối quan trọng khi mua.", 400, self.buy_radio_scanner, "has_radio_scanner"),
            ("Băng ghi âm giả mạo", "Tuồn tang vật ra Chợ Đen cuối đêm mà KHÔNG BỊ TĂNG Độ nghi ngờ.", 280, self.buy_fake_tape, "has_fake_tape")
        ]

        canvas = tk.Canvas(shop_card, bg=self.PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(shop_card, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.PANEL)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(frame_id, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        r_row = tk.Frame(scrollable_frame, bg=self.PANEL2, highlightbackground=self.BORDER, highlightthickness=1)
        r_row.pack(fill="x", padx=15, pady=4, ipady=2)
        r_info = tk.Frame(r_row, bg=self.PANEL2)
        r_info.pack(side="left", padx=10)
        tk.Label(r_info, text=f"{recipe_name} - ${recipe_cost}", font=("Segoe UI", 10, "bold"), fg=self.GOLD, bg=self.PANEL2).pack(anchor="w")
        tk.Label(r_info, text=recipe_desc, font=("Segoe UI", 8), fg=self.MUTED, bg=self.PANEL2).pack(anchor="w")
        r_btn = self.make_button(r_row, recipe_text, self.buy_recipe, width=12, bg="#248f57", state=recipe_state)
        r_btn.pack(side="right", padx=10)

        for name, desc, cost, cmd, key in items:
            row = tk.Frame(scrollable_frame, bg=self.PANEL2, highlightbackground=self.BORDER, highlightthickness=1)
            row.pack(fill="x", padx=15, pady=4, ipady=2)

            info = tk.Frame(row, bg=self.PANEL2)
            info.pack(side="left", padx=10)

            tk.Label(info, text=f"{name} - ${cost}", font=("Segoe UI", 10, "bold"), fg=self.GOLD, bg=self.PANEL2).pack(anchor="w")
            tk.Label(info, text=desc, font=("Segoe UI", 8), fg=self.MUTED, bg=self.PANEL2).pack(anchor="w")

            btn_state = "normal"
            btn_text = "MUA"
            if getattr(self, key, False):
                btn_state, btn_text = "disabled", "ĐÃ MUA"

            btn = self.make_button(row, btn_text, lambda c=cmd: c(), width=12, bg="#248f57", state=btn_state)
            btn.pack(side="right", padx=10)

        btn_next = self.make_button(outer, f"BẮT ĐẦU ĐÊM {self.night} ->", self.start_next_night, width=28, height=2, bg="#167c63")
        btn_next.pack(pady=10)

    def buy_wooden_tables(self):
        if self.money >= 200:
            self.money -= 200; self.has_wooden_tables = True
            messagebox.showinfo("Cửa hàng", "Đã mua Bàn Ghế Gỗ Sưa!\nTăng 10% tỷ lệ Khách VIP và bo thêm $10 mỗi phần ăn.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_ceiling_fan(self):
        if self.money >= 160:
            self.money -= 160; self.has_ceiling_fan = True
            messagebox.showinfo("Cửa hàng", "Đã lắp Quạt Trần Công Nghiệp!\nPhục vụ đúng món giúp giảm thêm 2% Độ nghi ngờ.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_iron_door(self):
        if self.money >= 220:
            self.money -= 220; self.has_iron_door = True
            messagebox.showinfo("Cửa hàng", "Đã lắp Cửa Sắt Cuốn Cường Lực!\nGiảm 30% Độ nghi ngờ bị phạt khi chọn sai đối thoại.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_meo_chieu_tai(self):
        if self.money >= 220:
            self.money -= 220; self.has_meo_chieu_tai = True
            messagebox.showinfo("Cửa hàng", "Đã mua Mèo Chiêu Tài!\nTỷ lệ Khách VIP tăng thêm +35% và bo thêm $25 khi phục vụ đúng món.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_bien_hieu_vip(self):
        if self.money >= 180:
            self.money -= 180; self.has_bien_hieu_vip = True
            messagebox.showinfo("Cửa hàng", "Đã mua Biển Hiệu Cơm Tấm VIP!\nTỷ lệ xuất hiện Khách VIP tăng thêm +15%.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_special_knife(self):
        if self.money >= 160:
            self.money -= 160; self.has_special_knife = True
            messagebox.showinfo("Cửa hàng", "Đã mua Dao Bếp Cao Cấp!\nPhục vụ đúng món được bo thêm $25.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_speaker(self):
        if self.money >= 150:
            self.money -= 150; self.has_speaker = True
            messagebox.showinfo("Cửa hàng", "Đã mua Loa Quảng Cáo Mini!\nTăng hiệu quả giảm độ nghi ngờ khi phục vụ đúng món.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_radio_detector(self):
        if self.money >= 250:
            self.money -= 250; self.has_radio_detector = True
            messagebox.showinfo("Cửa hàng", "Đã mua Radio Rà Sóng!\nBáo động ngay nếu đêm nay Cảnh sát bị giăng bẫy ngược.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_light(self):
        if self.money >= 120: 
            self.money -= 120; self.has_light = True
            messagebox.showinfo("Cửa hàng", "Đã mua Bóng đèn công suất lớn!\nKhông còn sợ sự cố cúp điện Đêm 3.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_recipe(self):
        if self.recipe_level == 0:
            if self.money >= 150:
                self.money -= 150
                self.recipe_level = 1
                self.serve_reward = 65
                messagebox.showinfo("Cửa hàng", "Đã nâng cấp Nước Mắm Bí Truyền Cấp 1!\nDoanh thu đĩa cơm tăng từ $45 -> $65.")
                self.check_achievements()
                self.build_shop_ui()
            else:
                messagebox.showwarning("Cửa hàng", "Bạn không đủ $150 để nâng cấp!")
        elif self.recipe_level == 1:
            if self.money >= 200:
                self.money -= 200
                self.recipe_level = 2
                self.serve_reward = 70
                messagebox.showinfo("Cửa hàng", "Đã nâng cấp Nước Mắm Bí Truyền Cấp 2!\nDoanh thu đĩa cơm tăng từ $65 -> $70.")
                self.check_achievements()
                self.build_shop_ui()
            else:
                messagebox.showwarning("Cửa hàng", "Bạn không đủ $200 để nâng cấp!")
        elif self.recipe_level == 2:
            if self.money >= 300:
                self.money -= 300
                self.recipe_level = 3
                self.serve_reward = 90
                messagebox.showinfo("Cửa hàng", "Đã nâng cấp Nước Mắm Bí Truyền Cấp 3 (MAX)!\nDoanh thu đĩa cơm tăng từ $70 -> $90.")
                self.check_achievements()
                self.build_shop_ui()
            else:
                messagebox.showwarning("Cửa hàng", "Bạn không đủ $300 để nâng cấp!")

    def buy_armor(self):
        if self.money >= 250: 
            self.money -= 250; self.has_armor = True; self.bought_armor_ever = True
            messagebox.showinfo("Cửa hàng", "Đã mua Áo giáp chống đạn!\nBảo vệ bạn 1 mạng khi Nghi ngờ chạm 100%.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_air_filter(self):
        if self.money >= 180: 
            self.money -= 180; self.has_air_filter = True; self.suspicion = max(0, self.suspicion - 15)
            messagebox.showinfo("Cửa hàng", "Đã mua Máy lọc không khí ngầm!\nLập tức giảm 15% Độ nghi ngờ.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_camera(self):
        if self.money >= 220: 
            self.money -= 220; self.has_camera = True
            messagebox.showinfo("Cửa hàng", "Đã lắp Camera ngụy trang mini!\nGiảm một nửa hình phạt khi phục vụ sai món.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_compartment_upgrade(self):
        if self.money >= 180:
            self.money -= 180; self.has_compartment_upgrade = True; self.max_compartment = 4
            messagebox.showinfo("Cửa hàng", "Đã nâng cấp Khoang bí mật!\nSức chứa tang vật tăng lên tối đa 4 gói.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_jammer(self):
        if self.money >= 200:
            self.money -= 200; self.has_jammer = True
            messagebox.showinfo("Cửa hàng", "Đã trang bị Phá sóng mini!\nAn toàn tuyệt đối khi từ chối nhận hàng ngầm.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_fake_docs(self):
        if self.money >= 200:
            self.money -= 200; self.has_fake_docs = True
            messagebox.showinfo("Cửa hàng", "Đã mua Tài liệu ngụy tạo!\nTự động trừ 10% Độ nghi ngờ ở đầu mỗi đêm.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_magnifier(self):
        if self.money >= 280:
            self.money -= 280; self.has_magnifier = True
            messagebox.showinfo("Cửa hàng", "Đã mua Kính lúp thám tử!\nTăng thời gian giải mã Kẻ Chỉ Điểm lên 45s.")
            self.check_achievements()
            self.build_shop_ui()

    def buy_vip_license(self):
        if self.money >= 350:
            self.money -= 350; self.has_vip_license = True
            messagebox.showinfo("Cửa hàng", "Đã mua Giấy phép kinh doanh VIP!\nGiờ đây mọi hình phạt khi sai món đều giảm 50%!")
            self.check_achievements()
            self.build_shop_ui()

    def buy_radio_scanner(self):
        if self.money >= 400:
            if self.clues >= self.max_clues:
                messagebox.showwarning("Cửa hàng", "Bạn đã có đủ 10 manh mối rồi, không cần thiết mua món này nữa!")
                return
            self.money -= 400; self.has_radio_scanner = True
            new_clue = self.add_clue()
            msg = f"Đã mua Máy quét vô tuyến!\nLập tức thu được thông tin quan trọng:\n+ {new_clue}"
            messagebox.showinfo("Tình báo cao cấp", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_fake_tape(self):
        if self.money >= 280:
            self.money -= 280; self.has_fake_tape = True
            messagebox.showinfo("Cửa hàng", "Đã mua Băng ghi âm giả mạo!\nTừ giờ có thể tuồn hàng chợ đen mà không sợ bị lộ tẩy.")
            self.check_achievements()
            self.build_shop_ui()

    def start_next_night(self):
        if self.suspicion < 15:
            base_pressure = random.randint(15, 30)
            self.suspicion = max(self.suspicion, base_pressure)

        if self.night >= 3 and random.random() < 0.25:
            self.police_compromised = True
            if self.has_radio_detector:
                messagebox.showwarning(
                    "⚠️ BÁO ĐỘNG RADIO RÀ SÓNG",
                    "Tín hiệu rà sóng phát hiện: Mạng lưới Cảnh sát đêm nay đã bị băng nhóm chiếm quyền kiểm soát!\n"
                    "TUYỆT ĐỐI KHÔNG GIAO HÀNG NGẦM CHO CẢNH SÁT TRONG ĐÊM NAY!"
                )
        else:
            self.police_compromised = False

        if getattr(self, "has_fake_docs", False) and self.night > 1:
            self.suspicion = max(0, self.suspicion - 10)
            
        self.build_game_ui()
        self.next_customer()

    def next_customer(self):
        if not self.game_running or self.in_arrest_mode:
            return

        self.talked_current_customer = False
        self.is_smuggler_customer = False

        vip_chance = 0.10
        if getattr(self, "has_meo_chieu_tai", False):
            vip_chance += 0.35
        if getattr(self, "has_bien_hieu_vip", False):
            vip_chance += 0.15
        if getattr(self, "has_wooden_tables", False):
            vip_chance += 0.10

        self.is_vip_customer = (random.random() < vip_chance)

        if random.random() < 0.20 and not self.informant_active and self.clues < self.max_clues and self.orders_completed_tonight > 0:
            self.trigger_informant_event()

        if random.random() < 0.35 and self.orders_completed_tonight > 0:
            self.is_smuggler_customer = True
            names_pool = ["Tên đàn em mặc áo đen", "Sứ giả băng nhóm áo khoác xám", "Lĩnh 'Đen' (Sát thủ trẻ)"]
            dialogues_pool = [
                "Boss gửi gói tang vật này, giấu kỹ dưới gầm bàn cho tao. Đừng để ai thấy!",
                "Hàng nóng đây, giữ hộ tao đến sáng mai. Có hậu tạ xứng đáng.",
                "Tao là Lĩnh 'Đen'. Trùm bảo cất gói này. Làm không cẩn thận tao cho sáng nhất đêm!"
            ]
        else:
            names_pool = [
                "Bà Cụ Bán Nước Mía (Bà Hai)", "Cậu Bé Đánh Giày (Bé Bo)",
                "Thiếu Úy Nam (Công An Khu Vực)", "Gã đàn ông áo khoác dính bùn",
                "Kẻ lạ mặt có vết sẹo trên cổ", "Gã khách quen mang chiếc túi nặng",
                "Tên thanh niên ngập ngừng, ánh mắt lạ", "Hành khách di chuyển lúc đêm muộn"
            ]
            dialogues_pool = [
                "Chú Hai ơi, tui thấy mấy thằng tay áo xăm xăm vừa rình mò sau hẻm đó...",
                "Chú ơi, con nhặt được tờ giấy chứa mã số này ở góc quầy...",
                "Tình hình an ninh dạo này khá phức tạp, anh bán cơm chú ý kẻ lạ nhé.",
                "Làm nhanh lên. Tao đang rất gấp.",
                "Nghe nói cảnh sát đang lùng Kiều Lương Tâm rất gắt.",
                "Đêm nay lạnh thật. Ngoài kia im lặng bất thường."
            ]

        toppings_pool = ["Sườn", "Trứng", "Chả", "Bì"]
        required_dishes = ["Cơm"] + random.sample(toppings_pool, k=random.randint(1, 3))

        raw_name = random.choice(names_pool)
        self.current_customer = {
            "name": raw_name,
            "dialog": random.choice(dialogues_pool),
            "required": required_dishes
        }
        self.customer_visual = self.customer_visual_from_name(raw_name)
        self.current_plate = []

        display_name = f"⭐ [KHÁCH VIP] {raw_name}" if self.is_vip_customer else raw_name

        self.lbl_canvas_status.config(text=f"Khách trước quầy: {display_name}")
        req = ", ".join(self.current_customer["required"])
        
        smuggler_note = ""
        if self.is_smuggler_customer:
            smuggler_note = "   |   ⚠️ [CÓ GÓI HÀNG NGẦM ĐÍNH KÈM]"
            self.btn_smuggled_action.config(state="normal", bg="#805ad5")
        else:
            self.btn_smuggled_action.config(state="disabled", bg="#384454")

        vip_note = "   |   ⭐ [KHÁCH VIP CÓ TIỀN BO]" if self.is_vip_customer else ""

        self.lbl_dialog.config(
            text=f"[{display_name}]\n\"{self.current_customer['dialog']}\"\n\n"
                 f"YÊU CẦU MÓN: [ {req} ]   |   Suất {self.orders_completed_tonight + 1}/5{smuggler_note}{vip_note}"
        )
        self.update_plate_display()
        self.update_stats()
        self.draw_counter_scene()

    def check_night_smuggler_dropoff(self):
        if len(self.hidden_compartment) > 0:
            count = len(self.hidden_compartment)
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Điểm hẹn giao hàng ngầm lúc 00:00")
            dialog.configure(bg=self.PANEL)
            self.center_window_dialog(dialog, 580, 320)
            dialog.grab_set()

            tk.Label(dialog, text=f"BẠN ĐANG GIỮ {count} GÓI TANG VẬT", font=self.title_font, fg=self.RED, bg=self.PANEL).pack(pady=(20, 10))
            tk.Label(dialog, text="Đã đến 00:00. Bạn sẽ xử lý số tang vật này như thế nào?", font=self.bold_font, fg=self.TEXT, bg=self.PANEL).pack(pady=(0, 20))

            def choice_police():
                if self.police_compromised:
                    penalty_susp = count * 20 + 25
                    self.suspicion += penalty_susp
                    self.unlocked_endings.add("Ending 7")
                    self.save_endings()
                    self.check_achievements()
                    messagebox.showerror(
                        "🚨 BẪY NGƯỢC CẢNH SÁT!",
                        f"Đồn cảnh sát đêm nay đã bị băng nhóm chiếm quyền!\n"
                        f"Tang vật bạn chuyển qua đã lọt trực tiếp vào tay nội gián. Ông trùm bắt đầu nghi ngờ thân phận bạn!\n\n"
                        f"- Mất toàn bộ tang vật\n"
                        f"- Độ nghi ngờ tăng vọt: +{penalty_susp}%"
                    )
                else:
                    bonus_money = count * 90
                    new_clue = self.add_clue()
                    self.money += bonus_money
                    msg = f"Tuồn cho đồng đội thành công!\n+ ${bonus_money} kinh phí chuyên án"
                    if new_clue:
                        msg += f"\n+ Khui tang vật tìm thấy: {new_clue}"
                    messagebox.showinfo("Trung thành", msg)
                self.finish_dropoff(dialog)

            def choice_black_market():
                bonus_money = count * 250
                penalty_suspicion = count * 15
                
                if self.has_fake_tape:
                    penalty_suspicion = 0
                    msg = f"Bán ra chợ đen trót lọt!\n+ ${bonus_money} lợi nhuận cá nhân\n\n(Dùng Băng ghi âm giả: Không bị tăng Độ nghi ngờ!)"
                else:
                    msg = f"Bán ra chợ đen trót lọt!\n+ ${bonus_money} lợi nhuận cá nhân\n- Tăng {penalty_suspicion}% Độ nghi ngờ từ hai phía!"
                    
                self.money += bonus_money
                self.suspicion += penalty_suspicion
                messagebox.showwarning("Sa ngã", msg)
                self.finish_dropoff(dialog)

            btn_frame = tk.Frame(dialog, bg=self.PANEL)
            btn_frame.pack(fill="x", pady=10)
            
            self.make_button(btn_frame, "GIAO CHO CẢNH SÁT\n(Kinh phí + Lấy Manh mối)", choice_police, width=25, bg="#248f57", height=3).pack(side="left", padx=15)
            self.make_button(btn_frame, "BÁN RA CHỢ ĐEN\n(Rất nhiều Tiền, Tăng nghi ngờ)", choice_black_market, width=25, bg="#8f2424", height=3).pack(side="right", padx=15)
            return 

        self.trigger_next_day_logic()

    def finish_dropoff(self, dialog):
        self.hidden_compartment.clear()
        dialog.destroy()
        if self.check_game_over():
            return
        self.trigger_next_day_logic()

    def trigger_ending(self, ending_code, title, description, is_win=False):
        self.unlocked_endings.add(ending_code)
        self.save_endings()
        self.check_achievements()
        
        if is_win:
            messagebox.showinfo(f"KẾT CỤC: {title}", description)
        else:
            messagebox.showerror(f"KẾT CỤC: {title}", description)
            
        self.game_running = False
        self.build_main_menu()

    def trigger_next_day_logic(self):
        self.check_achievements()
        if self.night < 6:
            messagebox.showinfo("Hoàn thành ca đêm", f"Đêm {self.night} kết thúc.\nChuyển sang nhiệm vụ ban ngày tiếp theo.")
            self.build_day_mission_ui(self.night)
        else:
            if self.clues >= 10:
                if self.suspicion >= 80:
                    self.trigger_ending("Ending 4", "BỊ BẰNG NHÓM XỬ LÝ (BAD ENDING)", "Thu thập đủ 10 manh mối nhưng Độ nghi ngờ quá cao làm lộ thân phận. Băng nhóm cho sát thủ thủ tiêu bạn trước khi chuyên án kích hoạt!")
                else:
                    messagebox.showinfo("Hoàn thành 6 đêm", "Bạn đã sống sót qua 6 đêm và thu thập đủ 10 manh mối! Sẵn sàng giăng bẫy bắt Kiều Lương Tâm!")
                    self.update_stats()
            else:
                if self.money >= 1000:
                    self.trigger_ending("Ending 2", "ÔM TIỀN TRỐN RA NƯỚC NGOÀI (ENDING ẨN)", "Nhận thấy bắt Kiều Lương Tâm quá rủi ro, bạn dùng số tiền kếch xù kiếm được mua vé máy bay sang Dubai, sống cuộc đời vương giả.")
                elif self.suspicion <= 25 and self.money >= 400:
                    self.trigger_ending("Ending 3", "VUA CƠM TẤM HOÀN LƯƠNG (ENDING ẨN)", "Bạn rút khỏi ngành cảnh sát, chính thức mở chuỗi quán Cơm Tấm danh tiếng, trở thành huyền thoại ẩm thực.")
                elif self.suspicion >= 75:
                    self.trigger_ending("Ending 4", "SÁT THỦ THỦ TIÊU (BAD ENDING)", "Độ nghi ngờ quá cao khiến Kiều Lương Tâm ra lệnh cho tay chân dọn dẹp quán cơm của bạn trong im lặng.")
                else:
                    self.trigger_ending("Ending 8", "NHIỆM VỤ THẤT BẠI (NORMAL ENDING)", "Bạn sống sót qua 6 đêm nhưng chỉ thu thập được " + str(self.clues) + "/10 manh mối. Chuyên án bị hủy bỏ, Kiều Lương Tâm tẩu thoát.")

    def action_arrest(self):
        if not self.game_running:
            return

        if self.night < 6:
            messagebox.showwarning("Chưa đủ thời gian", "Bạn phải bám trụ qua đủ 6 đêm để thu thập hồ sơ!")
            return

        if self.clues < 10:
            messagebox.showerror("Chưa đủ manh mối", f"Bạn mới có {self.clues}/10 manh mối. Cần đủ 10 manh mối để giăng bẫy Kiều Lương Tâm!")
            return

        if not self.in_arrest_mode:
            self.in_arrest_mode = True
            self.arrest_step = 1
            self.kitchen_frame.pack_forget()
            self.btn_investigate.config(state="disabled")
            self.btn_talk.config(state="disabled")
            self.btn_smuggled_action.config(state="disabled")
            self.btn_mindmap.config(state="disabled")
            self.btn_arrest.config(text="TIẾP TỤC VÂY BẮT", bg="#167c63")
            self.lbl_canvas_status.config(text="CHUYÊN ÁN: ĐÊM THỨ 6 - CẮT LƯỚI TOÀN DIỆN")

        if self.arrest_step == 1:
            self.lbl_dialog.config(text="[BƯỚC 1: HỘI QUÂN ĐẶC NHIỆM]\n\nVới đủ 10 manh mối đắt giá, lực lượng đặc nhiệm đã khép chặt vòng vây sào huyệt Kiều Lương Tâm.")
            self.arrest_step = 2
        elif self.arrest_step == 2:
            self.lbl_dialog.config(text="[BƯỚC 2: TIẾN VÀO SÀO HUYỆT]\n\nBạn bước thẳng vào phòng làm việc trung tâm. Kiều Lương Tâm đang ngồi chờ sẵn với nụ cười lạnh ngắt.")
            self.arrest_step = 3
        elif self.arrest_step == 3:
            self.lbl_dialog.config(text="[BƯỚC 3: ĐỐI ĐẦU TRỰC DIỆN]\n\nKIỀU LƯƠNG TÂM: 'Mày nghĩ qua mặt được tao sao? Hãy quy hàng hợp tác hoặc kết thúc tại đây.'")
            self.arrest_step = 4
        elif self.arrest_step == 4:
            if messagebox.askyesno(
                "Lựa Chọn Định Mệnh (Đêm 6) - Q-HouseTeam",
                "Bạn sẽ phát tín hiệu tấn công quyết định hay chấp nhận thương lượng?"
            ):
                self.trigger_ending("Ending 6", "THẮNG LỢI VINH QUANG (TRUE ENDING)", "Bạn ra lệnh: 'Tất cả đứng im, Cảnh sát đây!' Cảnh sát đặc nhiệm ập vào bắt gọn Kiều Lương Tâm!", is_win=True)
            else:
                self.trigger_ending("Ending 5", "KẾT CỤC BUỒN (SẬP BẪY DO DỰ)", "Sự do dự phút cuối khiến bạn sập bẫy của Kiều Lương Tâm và bị bắt làm con nợ.", is_win=False)

        self.draw_counter_scene()

    def check_game_over(self):
        if self.suspicion >= 100:
            if self.has_armor:
                self.has_armor = False
                self.suspicion = 60
                messagebox.showwarning("Áo giáp cứu mạng", "Độ nghi ngờ chạm 100%! Áo giáp chống đạn giúp bạn thoát chết. Độ nghi ngờ giảm về 60%.")
                return False
            else:
                self.trigger_ending("Ending 1", "THÂN PHẬN BỊ LẬT TẨY (GAME OVER)", "Độ nghi ngờ chạm 100%. Thân phận cảnh sát chìm của bạn hoàn toàn bị phơi bày!")
                return True
        return False

    def execute_day_mission(self, reward_money, reward_clue, susp_change):
        if reward_money < 0 and self.money < abs(reward_money):
            messagebox.showwarning("Không đủ tiền", "Bạn không đủ vốn để thực hiện phương án tốn phí này!")
            return

        self.money += reward_money
        clue_msg = ""
        if reward_clue > 0:
            for _ in range(reward_clue):
                new_c = self.add_clue()
                if new_c:
                    clue_msg += f"\n+ Vật chứng: {new_c}"

        self.suspicion = max(0, min(100, self.suspicion + susp_change))
        msg = f"Nhiệm vụ ban ngày hoàn tất!\n\n• Biến động tài chính: ${reward_money}{clue_msg}\n• Độ nghi ngờ thay đổi: {susp_change}%"
        messagebox.showinfo("Kết quả nhiệm vụ ban ngày", msg)

        self.night += 1
        self.orders_completed_tonight = 0
        self.hour, self.minute = 20, 0
        self.check_achievements()
        self.build_shop_ui()

    def build_day_mission_ui(self, day):
        self.clear_root()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=40, pady=25)

        tk.Label(outer, text=f"BAN NGÀY - NHIỆM VỤ MỞ RỘNG (SÁNG SAU ĐÊM {day})", font=("Segoe UI", 18, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(10, 2))
        tk.Label(outer, text="CREATOR BY: Q-HOUSETEAM | Lựa chọn trinh sát ngầm cẩn trọng.", font=("Segoe UI", 10), fg=self.CYAN, bg=self.BG).pack(pady=(0, 15))

        card = tk.Frame(outer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, ipadx=15, ipady=10)

        missions = {
            1: (
                "NHIỆM VỤ 1: DO THÁM CHỢ ĐẦU MỐI",
                "Phát hiện xe tải đông lạnh không biển số bốc dỡ hàng hóa lạ lúc rạng sáng.",
                [
                    ("1. Lén lút ghi nhận biển số & lịch trình", "Thu thập thông tin phương tiện vận chuyển.\n-> Thưởng +$60 kinh phí & +1 Manh mối!", 60, 1, 0),
                    ("2. Tiếp cận dò hỏi trực tiếp tài xế", "Lấy thông tin nhanh nhưng dễ bị chú ý.\n-> Thưởng +$110 kinh phí nhưng tăng 12% Độ nghi ngờ.", 110, 0, 12),
                    ("3. Lặng lẽ rút lui bảo đảm an toàn", "Giữ vững thân phận an toàn tuyệt đối.\n-> Giảm 10% Độ nghi ngờ.", 0, 0, -10),
                    ("4. Hối lộ bảo vệ khu vực bốc dỡ (Tốn $20)", "Đột nhập sâu vào khu vực cấm.\n-> Nhận +1 Manh mối và +$40, nhưng tốn phí.", -20, 1, 5)
                ]
            ),
            2: (
                "NHIỆM VỤ 2: GIẢI MÃ THƯ MẬT",
                "Thu được đoạn mã liên lạc từ tay chân băng nhóm: 'KLT-1082-SÁI-SÀO'",
                [
                    ("1. Truy vết tọa độ sào huyệt nhà kho", "Định vị khu vực tập kết tội phạm.\n-> Nhận ngay +1 Manh mối!", 0, 1, 0),
                    ("2. Theo dõi dòng tài khoản đen", "Phong tỏa nguồn tài chính bất hợp pháp.\n-> Thưởng +$130 kinh phí!", 130, 0, 0),
                    ("3. Tung tin đồn giả làm nhiễu loạn", "Đánh lạc hướng lực lượng theo dõi.\n-> Giảm mạnh 18% Độ nghi ngờ.", 0, 0, -18),
                    ("4. Giải mã bằng phần mềm chuyên dụng (Tốn $30)", "Thu thập thông tin cao cấp.\n-> Nhận ngay +1 Manh mối & Thưởng +$80!", 80, 1, 2)
                ]
            ),
            3: (
                "NHIỆM VỤ 3: TIẾP CẬN CƠ SỞ CUNG ỨNG",
                "Phát hiện một cơ sở phụ chuyên cung cấp nguyên liệu mờ ám cho quán của Kiều Lương Tâm.",
                [
                    ("1. Đột nhập thu thập sổ sách giao dịch", "Thu thập bằng chứng tài chính trực tiếp.\n-> Nhận +1 Manh mối và +$70!", 70, 1, 5),
                    ("2. Móc nối với nhân viên kho bên trong", "Mua chuộc nội gián để lấy tin nội bộ.\n-> Thưởng +$90 kinh phí chuyên án.", 90, 0, 0),
                    ("3. Quan sát từ xa tránh bị phát hiện", "Giữ an toàn tuyệt đối cho thân phận.\n-> Giảm 12% Độ nghi ngờ.", 0, 0, -12),
                    ("4. Cài thiết bị nghe lén vào kho hàng (Tốn $40)", "Theo dõi toàn bộ động tĩnh băng nhóm.\n-> Nhận +1 Manh mối và +$50!", 50, 1, 4)
                ]
            ),
            4: (
                "NHIỆM VỤ 4: ĐIỀU TRA KHO HÀNG NGOẠI Ô",
                "Bám theo nghi phạm đến một kho hàng cũ ở vùng ven thành phố.",
                [
                    ("1. Chụp ảnh tư liệu hoạt động đáng ngờ", "Tư liệu sống động cho hồ sơ.\n-> Nhận +1 Manh mối quan trọng!", 0, 1, 0),
                    ("2. Trấn áp nhẹ một tên lính canh lấy lời khai", "Thu thập thông tin nhanh chóng bằng bạo lực.\n-> Thưởng +$120 nhưng tăng 15% Độ nghi ngờ.", 120, 0, 15),
                    ("3. Rút lui củng cố kế hoạch vây bắt", "Bảo toàn lực lượng tối đa.\n-> Giảm 12% Độ nghi ngờ.", 0, 0, -12),
                    ("4. Đột nhập phòng máy chủ sao lưu dữ liệu (Tốn $50)", "Lấy toàn bộ hồ sơ tội phạm.\n-> Nhận +1 Manh mối & Thưởng +$90!", 90, 1, 8)
                ]
            ),
            5: (
                "NHIỆM VỤ 5: CHUẨN BỊ TRẬN QUYẾT CHIẾN",
                "Đêm cuối cùng trước khi giăng bẫy toàn bộ băng nhóm. Toàn đội trực chiến.",
                [
                    ("1. Rà soát lại hồ sơ tình báo", "Kiểm tra độ chính xác hồ sơ.\n-> Nhận +1 Manh mối hoàn thiện cuối cùng!", 0, 1, 0),
                    ("2. Huy động thêm quỹ dự phòng chuyên án", "Đảm bảo tài chính cho đội đặc nhiệm.\n-> Thưởng +$180 kinh phí lớn!", 180, 0, 0),
                    ("3. Kiểm tra thiết bị phòng hộ cá nhân", "Tăng cường an toàn tối đa cho bản thân.\n-> Giảm 25% Độ nghi ngờ.", 0, 0, -25),
                    ("4. Tổ chức họp kín với đội đặc nhiệm cấp cao (Tốn $60)", "Lên phương án đánh úp hoàn hảo.\n-> Nhận +1 Manh mối & Thưởng +$100!", 100, 1, 5)
                ]
            )
        }

        title, story, options = missions.get(day, missions[1])

        tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), fg=self.CYAN, bg=self.PANEL).pack(anchor="w", padx=12, pady=(8, 4))
        tk.Label(card, text=story, font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL, wraplength=850, justify="left").pack(anchor="w", padx=12, pady=(0, 10))

        options_container = tk.Frame(card, bg=self.PANEL)
        options_container.pack(fill="x", padx=5, pady=2)

        for opt_title, opt_desc, reward_money, reward_clue, susp_change in options:
            row = tk.Frame(options_container, bg=self.PANEL2, highlightbackground=self.BORDER, highlightthickness=1)
            row.pack(fill="x", padx=8, pady=4)

            info = tk.Frame(row, bg=self.PANEL2)
            info.pack(side="left", padx=10, pady=5)

            tk.Label(info, text=opt_title, font=("Segoe UI", 9, "bold"), fg=self.GOLD, bg=self.PANEL2).pack(anchor="w")
            tk.Label(info, text=opt_desc, font=("Segoe UI", 8), fg=self.MUTED, bg=self.PANEL2).pack(anchor="w")

            cmd = lambda rm=reward_money, rc=reward_clue, sc=susp_change: self.execute_day_mission(rm, rc, sc)
            self.make_button(row, "CHỌN", cmd, width=10, bg="#2b6cb0").pack(side="right", padx=10)

    def action_talk_customer(self):
        if not self.game_running or not self.current_customer or self.in_arrest_mode:
            return
        if self.talked_current_customer:
            messagebox.showinfo("Đối thoại", "Bạn đã trò chuyện với vị khách này rồi.")
            return

        dialog_win = tk.Toplevel(self.root)
        dialog_win.title("Lựa Chọn Đối Thoại Phân Nhánh - Q-HouseTeam")
        dialog_win.configure(bg=self.PANEL)
        dialog_win.transient(self.root)
        dialog_win.grab_set()
        self.center_window_dialog(dialog_win, 600, 420)

        c_name = self.current_customer["name"]
        tk.Label(dialog_win, text=f"ĐỐI THOẠI: {c_name.upper()}", font=("Segoe UI", 13, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(15, 5))
        tk.Label(dialog_win, text=f"\"...{self.current_customer['dialog']}\"", font=("Segoe UI", 10, "italic"), fg=self.TEXT, bg=self.PANEL, wraplength=540).pack(pady=(0, 15))

        if "Bà Cụ Bán Nước Mía" in c_name:
            options = [
                ("1. Lắng nghe dặn dò chu đáo", "Cụ Hai chia sẻ thông tin rình mò.\n-> Giảm 10% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 101)),
                ("2. Mua giúp cụ ly nước mía ($10)", "Ủng hộ cụ bớt vất vả.\n-> Thưởng +1 Manh mối từ cụ!", lambda: self.choose_dialogue(dialog_win, 102)),
                ("3. Lờ đi không quan tâm", "Cụ lắc đầu rời đi.\n-> Không thay đổi.", lambda: self.choose_dialogue(dialog_win, 103))
            ]
        elif "Cậu Bé Đánh Giày" in c_name:
            options = [
                ("1. Cho em bé ăn miễn phí đĩa cơm", "Em bé rối rít cảm ơn.\n-> Trao cho bạn mảnh giấy chứa Manh mối!", lambda: self.choose_dialogue(dialog_win, 201)),
                ("2. Hỏi xem em nhặt giấy ở đâu", "Bé Bo chỉ chỗ góc tối bến xe.\n-> Giảm 8% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 202)),
                ("3. Cho ít tiền lẻ ($5)", "Bé vui vẻ chúc chú bán đắt hàng.\n-> Thưởng +$15 may mắn.", lambda: self.choose_dialogue(dialog_win, 203))
            ]
        elif "Thiếu Úy Nam" in c_name:
            options = [
                ("1. Báo cáo tình hình an ninh tốt", "Đồng nghiệp an tâm rời đi.\n-> Giảm 12% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 301)),
                ("2. Nháy ám hiệu trinh sát ngầm", "Thiếu úy Nam hiểu ý bắt tay.\n-> Hỗ trợ +$50 kinh phí secret.", lambda: self.choose_dialogue(dialog_win, 302)),
                ("3. Giữ thái độ lúng túng", "Thiếu úy nghi ngờ quan sát kỹ.\n-> Tăng 10% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 303))
            ]
        else:
            options = [
                ("1. Thân thiện & Chu đáo", "Phục vụ lịch sự, nhẹ nhàng.\n-> Giảm 5% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 1)),
                ("2. Tra hỏi ngầm tinh tế", "Dò hỏi thông tin về tổ chức.\n-> 50% Manh mối | 50% Khách tức giận.", lambda: self.choose_dialogue(dialog_win, 2)),
                ("3. Dùng ám hiệu giang hồ (Tốn $15)", "Sử dụng từ lóng ngầm.\n-> Giảm mạnh 15% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 3))
            ]

        for title, desc, cmd in options:
            btn_frame = tk.Frame(dialog_win, bg=self.PANEL2, highlightbackground=self.BORDER, highlightthickness=1)
            btn_frame.pack(fill="x", padx=20, pady=5)

            sub = tk.Frame(btn_frame, bg=self.PANEL2)
            sub.pack(side="left", padx=10, pady=5)
            tk.Label(sub, text=title, font=("Segoe UI", 9, "bold"), fg=self.CYAN, bg=self.PANEL2).pack(anchor="w")
            tk.Label(sub, text=desc, font=("Segoe UI", 8), fg=self.MUTED, bg=self.PANEL2).pack(anchor="w")

            self.make_button(btn_frame, "CHỌN", cmd, width=10, bg="#2b6cb0").pack(side="right", padx=10)

    def apply_susp_penalty(self, val):
        if getattr(self, "has_iron_door", False):
            val = max(1, int(val * 0.7))
        self.suspicion += val
        return val

    def choose_dialogue(self, win, option):
        win.destroy()
        self.talked_current_customer = True

        if option == 1:
            self.suspicion = max(0, self.suspicion - 5)
            msg = "Bạn mỉm cười phục vụ. Khách hàng tỏ ra hài lòng. (Độ nghi ngờ giảm 5%)"
        elif option == 2:
            if random.random() < 0.5:
                new_clue = self.add_clue()
                if new_clue:
                    msg = f"Khách hàng vô tình hé lộ chi tiết đắt giá!\n\n(Thu được: {new_clue}! Tổng: {self.clues}/{self.max_clues})"
                else:
                    msg = "Khách hàng trò chuyện bình thường không có thông tin mới."
            else:
                p = self.apply_susp_penalty(15)
                msg = f"Lời dò hỏi quá lộ liễu khiến khách nghi ngờ!\n\n(Độ nghi ngờ tăng {p}%)"
        elif option == 3:
            if self.money >= 15:
                self.money -= 15
                self.suspicion = max(0, self.suspicion - 15)
                msg = "Dùng ám hiệu thành công. (Tốn $15 - Độ nghi ngờ giảm 15%)"
            else:
                msg = "Không đủ tiền thực hiện ám hiệu ($15)."
        elif option == 101:
            self.suspicion = max(0, self.suspicion - 10)
            msg = "Bà Hai nhắc nhở cẩn thận bọn xăm trổ. (Độ nghi ngờ giảm 10%)"
        elif option == 102:
            if self.money >= 10:
                self.money -= 10
                new_clue = self.add_clue()
                msg = f"Cụ Hai cảm động đưa mảnh giấy nhặt được sau bến xe!\n\n(Thu được: {new_clue})" if new_clue else "Cụ Hai cảm ơn bạn chu đáo."
            else:
                msg = "Bạn không đủ $10 để mua nước mía."
        elif option == 103:
            msg = "Bà Hai lẳng lặng đi qua."
        elif option == 201:
            new_clue = self.add_clue()
            msg = f"Bé Bo ăn cơm ngon lành và trao tờ giấy ghi chép mật mã!\n\n(Thu được: {new_clue})" if new_clue else "Bé Bo rối rít cảm ơn đĩa cơm ấm áp."
        elif option == 202:
            self.suspicion = max(0, self.suspicion - 8)
            msg = "Bé Bo chỉ góc hẻm tối nơi tay sai tập kết. (Độ nghi ngờ giảm 8%)"
        elif option == 203:
            if self.money >= 5:
                self.money += 10
                msg = "Bé Bo vui vẻ tặng bạn đồng xu may mắn! (+ $10)"
            else:
                msg = "Bạn không có đủ $5."
        elif option == 301:
            self.suspicion = max(0, self.suspicion - 12)
            msg = "Thiếu úy Nam gật đầu yên tâm quay về đồn. (Độ nghi ngờ giảm 12%)"
        elif option == 302:
            self.money += 50
            msg = "Thiếu úy Nam ngầm tiếp viện kinh phí trinh sát. (+ $50)"
        elif option == 303:
            p = self.apply_susp_penalty(10)
            msg = f"Thái độ lúng túng làm công an khu vực chú ý. (Độ nghi ngờ +{p}%)"

        self.lbl_dialog.config(text=f"[KẾT QUẢ ĐỐI THOẠI]\n\n{msg}")
        self.check_game_over()
        self.check_achievements()
        self.update_stats()

    def action_investigate(self):
        if not self.game_running or self.in_arrest_mode:
            return
        if self.clues >= self.max_clues:
            messagebox.showinfo("Manh mối", f"Bạn đã thu thập đủ tối đa {self.max_clues} manh mối.")
            return

        success_rate = 0.8 if getattr(self, "has_magnifier", False) else 0.5
        if random.random() < success_rate:
            new_clue = self.add_clue()
            if new_clue:
                messagebox.showinfo("Tìm thấy manh mối", f"Thu thập thành công vật chứng:\n[{new_clue}]\n\nTiến độ: {self.clues}/{self.max_clues}")
        else:
            self.suspicion += 20
            messagebox.showwarning("Suýt bị lộ", "Có kẻ nghi ngờ hành động điều tra của bạn. Độ nghi ngờ tăng 20%.")

        if self.check_game_over():
            return
        self.check_achievements()
        self.update_stats()

    def action_take_smuggled_package(self):
        if not self.is_smuggler_customer:
            return

        if len(self.hidden_compartment) >= self.max_compartment:
            self.suspicion += 40
            self.is_smuggler_customer = False
            self.btn_smuggled_action.config(state="disabled", bg="#384454")
            messagebox.showerror(
                "QUÁ TẢI KHOANG BÍ MẬT!",
                f"Khoang cất giấu đã đầy ({self.max_compartment}/{self.max_compartment})! Tang vật rơi ra ngoài khiến khách hàng phát hiện!\n\n(Độ nghi ngờ +40%)"
            )
            self.check_game_over()
            self.update_stats()
            return

        self.hidden_compartment.append("Gói hàng phi pháp")
        self.money += 40  
        self.is_smuggler_customer = False
        self.btn_smuggled_action.config(state="disabled", bg="#384454")
        
        messagebox.showinfo(
            "Đã cất giấu thành công",
            f"Bạn đã lén giấu gói hàng ngầm vào khoang gầm bàn.\n• Nhận trước: +$40 tiền công\n• Khoang bí mật: [{len(self.hidden_compartment)}/{self.max_compartment}]"
        )
        self.check_achievements()
        self.update_stats()

    def add_ing(self, item):
        if not self.game_running or self.in_arrest_mode:
            return
        self.current_plate.append(item)
        self.update_plate_display()

    def reset_plate(self):
        if self.in_arrest_mode:
            return
        self.current_plate = []
        self.update_plate_display()

    def update_plate_display(self):
        if hasattr(self, "lbl_plate"):
            self.lbl_plate.config(text=f"Đĩa cơm đang làm: [ Trống ]" if not self.current_plate else f"Đĩa cơm đang làm: [ {', '.join(self.current_plate)} ]")
        if hasattr(self, "lbl_compartment"):
            self.lbl_compartment.config(text=f"Khoang ngầm: [{len(self.hidden_compartment)}/{self.max_compartment}]")

    def serve_plate(self):
        if not self.game_running or not self.current_customer or self.in_arrest_mode:
            return

        if self.is_smuggler_customer:
            if not self.has_jammer:
                self.suspicion += 10
                messagebox.showwarning("Từ chối ngầm", "Bạn lờ đi gói hàng và chỉ phục vụ cơm. Tên đàn em lườm nguýt bỏ đi. (Độ nghi ngờ +10%)")
            else:
                messagebox.showinfo("Từ chối an toàn", "Nhờ có Thiết bị phá sóng mini, khách ngậm ngùi bỏ đi mà không thể báo động. (Không tăng nghi ngờ)")
            self.is_smuggler_customer = False
            self.btn_smuggled_action.config(state="disabled", bg="#384454")

        required = self.current_customer["required"]
        if sorted(self.current_plate) == sorted(required):
            total_earned = self.serve_reward
            bonus_notes = []

            if self.has_special_knife:
                total_earned += 25
                bonus_notes.append("+$25 Dao bếp cao cấp")

            if self.has_meo_chieu_tai:
                total_earned += 25
                bonus_notes.append("+$25 Mèo chiêu tài")

            if getattr(self, "has_wooden_tables", False):
                total_earned += 10
                bonus_notes.append("+$10 Bàn ghế gỗ sưa")

            if self.is_vip_customer:
                vip_bonus = 35
                total_earned += vip_bonus
                bonus_notes.append(f"+${vip_bonus} Khách VIP bo")

            self.money += total_earned
            
            susp_reduce = 8 + (4 if self.has_speaker else 0) + (2 if getattr(self, "has_ceiling_fan", False) else 0)
            self.suspicion = max(0, self.suspicion - susp_reduce)
            
            self.orders_completed_tonight += 1
            self.advance_time()

            bonus_msg = f" ({', '.join(bonus_notes)})" if bonus_notes else ""
            messagebox.showinfo("Thành công", f"Phục vụ đúng món. Khách trả ${total_earned}{bonus_msg}.")
        else:
            self.money -= 10
            base_penalty = 40 if (self.night == 3 and not self.has_light) else 20
            susp_penalty = int(base_penalty * 0.5) if self.has_camera else base_penalty
            if self.has_vip_license:
                susp_penalty = susp_penalty // 2
                
            self.suspicion += susp_penalty
            self.advance_time()
            messagebox.showwarning("Sai món", f"Khách bực mình vì sai món!\n(Phạt Độ nghi ngờ: +{susp_penalty}%)")

        if self.check_game_over():
            return

        self.check_achievements()

        if self.orders_completed_tonight >= 5:
            self.check_night_smuggler_dropoff()
            return

        self.update_stats()
        self.next_customer()

    def advance_time(self):
        self.minute += 48
        if self.minute >= 60:
            self.hour += 1
            self.minute -= 60

    def confirm_back_menu(self):
        if messagebox.askyesno("Về menu", "Bạn có chắc muốn rời chuyên án? Tiến trình sẽ bị mất."):
            self.build_main_menu()

    def customer_visual_from_name(self, name):
        visuals = {
            "Bà Cụ Bán Nước Mía (Bà Hai)": {"skin": "#d9a982", "hair": "#e2e8f0", "shirt": "#4a5568", "style": "short", "scar": False, "glasses": True},
            "Cậu Bé Đánh Giày (Bé Bo)": {"skin": "#edbc92", "hair": "#1a202c", "shirt": "#2b6cb0", "style": "fringe", "scar": False, "glasses": False},
            "Thiếu Úy Nam (Công An Khu Vực)": {"skin": "#d7a47d", "hair": "#111318", "shirt": "#22543d", "style": "buzz", "scar": False, "glasses": False},
            "Lĩnh 'Đen' (Sát thủ trẻ)": {"skin": "#c78d6e", "hair": "#171923", "shirt": "#1a202c", "style": "hood", "scar": True, "glasses": False},
            "Gã đàn ông áo khoác dính bùn": {"skin": "#d7a47d", "hair": "#181a1f", "shirt": "#39424e", "style": "short", "scar": False, "glasses": False},
            "Kẻ lạ mặt có vết sẹo trên cổ": {"skin": "#c78d6e", "hair": "#111318", "shirt": "#2d3139", "style": "buzz", "scar": True, "glasses": False},
            "Gã khách quen mang chiếc túi nặng": {"skin": "#d9a982", "hair": "#5b3a25", "shirt": "#534734", "style": "swept", "scar": False, "glasses": True},
            "Tên thanh niên ngập ngừng, ánh mắt lạ": {"skin": "#edbc92", "hair": "#25262a", "shirt": "#31465f", "style": "fringe", "scar": False, "glasses": False},
            "Hành khách di chuyển lúc đêm muộn": {"skin": "#b97859", "hair": "#1a1b20", "shirt": "#3e3c4a", "style": "cap", "scar": False, "glasses": True}
        }
        return visuals.get(name, visuals["Gã đàn ông áo khoác dính bùn"])

    def draw_face(self, canvas, cx, cy, visual, label=None, scale=1.0):
        skin = visual["skin"]
        hair = visual["hair"]
        shirt = visual["shirt"]
        r = int(40 * scale)

        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=skin, outline="#0c0f13", width=2)
        canvas.create_rectangle(cx - int(r * 1.55), cy + int(r * 0.8), cx + int(r * 1.55), cy + int(r * 2.5), fill=shirt, outline="#0c0f13", width=2)

        style = visual["style"]
        if style == "short":
            canvas.create_arc(cx - r, cy - r, cx + r, cy + int(r * 0.5), start=0, extent=180, fill=hair, outline=hair)
        elif style == "buzz":
            canvas.create_oval(cx - r, cy - r, cx + r, cy - int(r * 0.35), fill=hair, outline=hair)
        elif style == "swept":
            canvas.create_polygon(cx - r, cy - int(r * 0.45), cx - int(r * 0.15), cy - r, cx + r, cy - int(r * 0.7), cx + int(r * 0.3), cy - int(r * 0.1), fill=hair, outline=hair)
        elif style == "fringe":
            canvas.create_polygon(cx - r, cy - int(r * 0.15), cx - int(r * 0.75), cy - r, cx + int(r * 0.9), cy - int(r * 0.85), cx + int(r * 0.1), cy - int(r * 0.15), fill=hair, outline=hair)
        elif style == "cap":
            canvas.create_arc(cx - r, cy - r, cx + r, cy + int(r * 0.2), start=0, extent=180, fill=hair, outline=hair)
            canvas.create_rectangle(cx - int(r * 0.95), cy - int(r * 0.65), cx + int(r * 0.95), cy - int(r * 0.35), fill="#20242c", outline="")
            canvas.create_rectangle(cx + int(r * 0.3), cy - int(r * 0.47), cx + int(r * 1.35), cy - int(r * 0.3), fill="#20242c", outline="")
        elif style == "hood":
            canvas.create_arc(cx - int(r * 1.25), cy - int(r * 1.2), cx + int(r * 1.25), cy + int(r * 1.1), start=0, extent=180, fill="#15181d", outline="#30353d", width=2)

        eye_y = cy - int(r * 0.08)
        eye_dx = int(r * 0.34)
        eye_r = max(2, int(r * 0.08))
        canvas.create_oval(cx - eye_dx - eye_r, eye_y - eye_r, cx - eye_dx + eye_r, eye_y + eye_r, fill="#111318", outline="")
        canvas.create_oval(cx + eye_dx - eye_r, eye_y - eye_r, cx + eye_dx + eye_r, eye_y + eye_r, fill="#111318", outline="")

        canvas.create_line(cx - int(r * 0.16), cy + int(r * 0.17), cx + int(r * 0.16), cy + int(r * 0.12), fill="#754d3d", width=max(1, int(2 * scale)))
        canvas.create_arc(cx - int(r * 0.3), cy + int(r * 0.22), cx + int(r * 0.3), cy + int(r * 0.52), start=200, extent=140, style="arc", outline="#653f35", width=max(1, int(2 * scale)))

        if visual.get("glasses"):
            frame = "#111318"
            canvas.create_oval(cx - int(r * 0.58), eye_y - int(r * 0.2), cx - int(r * 0.05), eye_y + int(r * 0.24), outline=frame, width=max(1, int(2 * scale)))
            canvas.create_oval(cx + int(r * 0.05), eye_y - int(r * 0.2), cx + int(r * 0.58), eye_y + int(r * 0.24), outline=frame, width=max(1, int(2 * scale)))
            canvas.create_line(cx - int(r * 0.05), eye_y, cx + int(r * 0.05), eye_y, fill=frame, width=max(1, int(2 * scale)))

        if visual.get("scar"):
            canvas.create_line(cx + int(r * 0.47), cy - int(r * 0.32), cx + int(r * 0.64), cy + int(r * 0.08), fill="#8f514d", width=max(1, int(3 * scale)))
            canvas.create_line(cx + int(r * 0.41), cy - int(r * 0.2), cx + int(r * 0.57), cy + int(r * 0.21), fill="#8f514d", width=max(1, int(1 * scale)))

        if label:
            canvas.create_text(cx, cy + int(r * 2.75), text=label, fill="#aab4c3", font=("Segoe UI", 9, "bold"))

    def draw_klt_face(self, canvas, cx, cy):
        r = 45
        canvas.create_oval(cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12, fill="#12151a", outline="#343a44", width=2)
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#b57e61", outline="#0b0d10", width=2)
        canvas.create_arc(cx - r, cy - r, cx + r, cy + int(r * 0.55), start=0, extent=180, fill="#17191d", outline="#17191d")
        canvas.create_text(cx, cy + 65, text="KIỀU LƯƠNG TÂM", fill=self.RED, font=("Segoe UI", 10, "bold"))

    def update_stats(self):
        if hasattr(self, "lbl_stats"):
            weather_str = self.get_weather_name()
            self.lbl_stats.config(
                text=f"GIỜ: {self.hour:02d}:{self.minute:02d}   |   "
                     f"ĐÊM {self.night}/6 [{weather_str}]   |   VỐN: ${self.money}   |   "
                     f"MANH MỐI: {self.clues}/{self.max_clues}   |   NGHI NGỜ: {self.suspicion}%"
            )
        if hasattr(self, "lbl_weather_info"):
            self.lbl_weather_info.config(text=f"THỜI TIẾT: {self.get_weather_description()}")
        if hasattr(self, "lbl_compartment"):
            self.lbl_compartment.config(text=f"Khoang ngầm: [{len(self.hidden_compartment)}/{self.max_compartment}]")

    def draw_counter_scene(self):
        if not hasattr(self, "canvas_view") or not self.canvas_view.winfo_exists():
            return

        self.canvas_view.delete("all")
        w = max(self.canvas_view.winfo_width(), 900)
        h = max(self.canvas_view.winfo_height(), 160)
        
        self.canvas_view.create_rectangle(0, 0, w, h, fill="#171a20", outline="")
        for x in range(40, w, 80):
            self.canvas_view.create_line(x, 25, x, 95, fill="#222731", width=2)
        
        self.canvas_view.create_rectangle(0, h - 55, w, h, fill="#3a2817", outline="")
        self.canvas_view.create_rectangle(w // 2 - 75, h - 90, w // 2 + 75, h - 55, fill="#282d35", outline="#555d68")

        cx, cy = w // 2, 58

        if self.in_arrest_mode:
            self.canvas_view.create_text(cx, 18, text="[SÀO HUYỆT ĐÊM THỨ 6 - QUYẾT CHIẾN]", fill="#ef6461", font=("Segoe UI", 11, "bold"))
            self.draw_klt_face(self.canvas_view, cx, 62)
        elif self.current_customer:
            display_name = f"⭐ [KHÁCH VIP] {self.current_customer['name']}" if getattr(self, "is_vip_customer", False) else self.current_customer["name"]
            self.draw_face(self.canvas_view, cx, cy, self.customer_visual, display_name, 0.8)

        if self.night == 3 and not self.has_light and not self.in_arrest_mode:
            self.canvas_view.create_rectangle(0, 0, w, h, fill="#000000", stipple="gray50")
            self.canvas_view.create_text(cx, h - 18, text="⚡ Cúp điện! (Cần Bóng đèn công suất lớn)", fill=self.GOLD, font=("Segoe UI", 9, "bold"))

        self.canvas_view.create_text(18, 15, anchor="nw", text="QUẦY BÁN - CREATOR BY: Q-HOUSETEAM (v1.1.0)", fill="#8d98a7", font=("Segoe UI", 9, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ComTam6NightsGame(root)
    root.mainloop()