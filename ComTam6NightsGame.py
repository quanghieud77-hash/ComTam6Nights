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
        self.root.title("ComTam6NightsGame")
        self.root.configure(bg=self.BG)
        self.root.minsize(980, 760)
        self.center_window(1100, 800)

        self.current_lang = "vi"

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

    def t(self, vi_text, en_text):
        """Hàm hỗ trợ dịch thuật ngôn ngữ"""
        return en_text if self.current_lang == "en" else vi_text

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "vi" else "vi"
        if getattr(self, "game_running", False):
            self.build_game_ui()
            self.update_stats()
            self.draw_counter_scene()
        else:
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
                msg = f"Congratulations! You unlocked achievement:\n\n🏆 [{name}]" if self.current_lang == "en" else f"Chúc mừng! Bạn đã đạt thành tựu danh giá:\n\n🏆 [{name}]"
                title_msg = "NEW ACHIEVEMENT UNLOCKED!" if self.current_lang == "en" else "🏆 THÀNH TỰU MỚI MỞ KHÓA!"
                messagebox.showinfo(title_msg, msg, parent=self.root)

    def show_achievements(self):
        self.check_achievements()
        text = f"TOTAL ACHIEVEMENTS: {len(self.unlocked_achievements)}/6\n\n" if self.current_lang == "en" else f"TỔNG SỐ THÀNH TỰU ĐÃ ĐẠT: {len(self.unlocked_achievements)}/6\n\n"
        for code, (title, desc) in self.achievement_database.items():
            status = ("✅ UNLOCKED" if self.current_lang == "en" else "✅ ĐÃ ĐẠT") if code in self.unlocked_achievements else ("🔒 Locked" if self.current_lang == "en" else "🔒 Chưa mở")
            text += f"• {title} -> [{status}]\n  {desc}\n\n"
        messagebox.showinfo("Achievements & Badges" if self.current_lang == "en" else "Thành Tựu & Huy Hiệu Phá Án", text)

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
        weathers_vi = {1: "TRỜI TỊNH", 2: "MƯA TẦM TÃ", 3: "CÚP ĐIỆN", 4: "GIÓ BÃO GIẬT", 5: "THANH TRA ĐỘT XUẤT", 6: "ĐÊM SINH TỬ"}
        weathers_en = {1: "CLEAR SKY", 2: "HEAVY RAIN", 3: "BLACKOUT", 4: "STORMY WIND", 5: "SURPRISE INSPECTION", 6: "FATEFUL NIGHT"}
        return weathers_en.get(self.night, "Normal") if self.current_lang == "en" else weathers_vi.get(self.night, "Bình thường")

    def get_weather_description(self):
        descs_vi = {
            1: "Đêm 1: Trời quang mây tịnh. Hoạt động bán hàng diễn ra bình thường.",
            2: "Đêm 2: Mưa tầm tã & Sương mù. Khách hàng cảnh giác hơn (+5% nghi ngờ khi làm lỗi).",
            3: "Đêm 3: Cúp điện chập chờn! Cần 'Bóng đèn công suất lớn' để tránh phạt gấp đôi nghi ngờ.",
            4: "Đêm 4: Gió bão giật mạnh! Khách hàng vội vã, dễ xảy ra sai sót.",
            5: "Đêm 5: Thanh tra đô thị kiểm tra diện rộng! Nghi ngờ tăng nhanh nếu sai sót.",
            6: "Đêm 6: Đêm quyết chiến cuối cùng! Thu thập đủ 10 manh mối để giăng bẫy toàn diện."
        }
        descs_en = {
            1: "Night 1: Clear sky. Normal business operations.",
            2: "Night 2: Heavy rain & fog. Customers are more alert (+5% suspicion on error).",
            3: "Night 3: Flickering blackout! Need 'High-power light bulb' to avoid double penalties.",
            4: "Night 4: Strong storm winds! Customers are hurried, errors likely.",
            5: "Night 5: Urban inspection! Suspicion increases rapidly on errors.",
            6: "Night 6: Final showdown night! Collect all 10 clues to set the trap."
        }
        return descs_en.get(self.night, "") if self.current_lang == "en" else descs_vi.get(self.night, "")

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

        # Nút chuyển đổi ngôn ngữ ở góc trên
        lang_btn_text = "🌐 Ngôn ngữ: Tiếng Việt" if self.current_lang == "vi" else "🌐 Language: English"
        self.make_button(top, lang_btn_text, self.toggle_language, width=24, bg="#3b4654").pack(anchor="ne", pady=(0, 5))

        tk.Label(top, text="ComTam6NightsGame", font=("Segoe UI", 32, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(5, 2))
        tk.Label(top, text="CREATOR BY: Q-HOUSETEAM", font=("Segoe UI", 12, "bold"), fg=self.CYAN, bg=self.BG).pack(pady=(0, 10))
        
        feat_sub = "v1.1.0: Shop Upgrades, Achievements, Mind Map Deduction." if self.current_lang == "en" else "Phiên bản v1.1.0: Trang Bị Nâng Cấp Quán, Thành Tựu & Huy Hiệu, Sơ Đồ Tư Duy."
        tk.Label(top, text=feat_sub, font=("Segoe UI", 10), fg=self.MUTED, bg=self.BG, justify="center").pack(pady=(0, 10))

        card = tk.Frame(top, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(ipadx=30, ipady=10)

        feat_title = "NEW FEATURES v1.1.0" if self.current_lang == "en" else "TÍNH NĂNG MỚI BẢN v1.1.0"
        feat_desc = (
            "• Restaurant Interior Upgrades: Premium Wood Tables, Industrial Ceiling Fan & Steel Roller Door.\n"
            "• Achievement & Badge System: Unlock 6 prestigious detective titles.\n"
            "• Mind Map Deduction: Connect collected clues to solve puzzles.\n"
            "• Detailed Story NPCs: Sugarcane Vendor, Shoeshine Boy, Lieutenant Nam, Black Linh...\n"
            "• Rich Endings (8 Endings): Discover hidden endings based on Money & Suspicion."
        ) if self.current_lang == "en" else (
            "• Nâng Cấp Nội Thất Quán: Bàn Ghế Gỗ Sưa, Quạt Trần Công Nghiệp & Cửa Sắt Cuốn Cường Lực.\n"
            "• Hệ Thống Thành Tựu & Huy Hiệu: Mở khóa 6 danh hiệu trinh sát cao quý.\n"
            "• Sơ Đồ Tư Duy (Mind Map Deduction): Ghép nối manh mối thu thập được để giải mã câu đố.\n"
            "• NPC Cốt Truyện Chi Tiết: Bà Cụ Bán Nước Mía, Cậu Bé Đánh Giày, Thiếu Úy Nam, Lĩnh 'Đen'...\n"
            "• Đa kết cục phong phú (8 Endings): Khám phá các Ending ẩn tùy thuộc Tiền & Nghi ngờ."
        )

        tk.Label(card, text=feat_title, font=("Segoe UI", 12, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(0, 6))
        tk.Label(card, text=feat_desc, font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL, justify="left").pack()

        buttons = tk.Frame(outer, bg=self.BG)
        buttons.pack(pady=10)

        b1 = "START OPERATION" if self.current_lang == "en" else "BẮT ĐẦU CHUYÊN ÁN"
        b2 = f"ENDINGS LIBRARY ({len(self.unlocked_endings)}/8)" if self.current_lang == "en" else f"THƯ VIỆN ENDING ({len(self.unlocked_endings)}/8)"
        b3 = f"ACHIEVEMENTS & BADGES ({len(self.unlocked_achievements)}/6)" if self.current_lang == "en" else f"THÀNH TỰU & HUY HIỆU ({len(self.unlocked_achievements)}/6)"
        b4 = "NIGHT 0 - TUTORIAL" if self.current_lang == "en" else "ĐÊM 0 - HUẤN LUYỆN"
        b5 = "QUIT GAME" if self.current_lang == "en" else "THOÁT GAME"

        self.make_button(buttons, b1, self.start_game, width=28, height=2, bg="#167c63").pack(pady=3)
        self.make_button(buttons, b2, self.show_endings, width=28, height=2, bg="#2b6cb0").pack(pady=3)
        self.make_button(buttons, b3, self.show_achievements, width=28, height=2, bg="#d97706").pack(pady=3)
        self.make_button(buttons, b4, self.start_night_0_tutorial, width=28, height=2, bg="#3b4654").pack(pady=3)
        self.make_button(buttons, b5, self.root.destroy, width=28, height=2, bg="#9c3d3d").pack(pady=3)

    def show_endings(self):
        end_names = [
            "Ending 1: Exposed Identity (GameOver)",
            "Ending 2: Escaping Abroad with Money (Hidden)",
            "Ending 3: Reformed Broken Rice King (Hidden)",
            "Ending 4: Assassinated (Bad End)",
            "Ending 5: Trapped by Last-Minute Hesitation",
            "Ending 6: Arresting Kieu Luong Tam (True End)",
            "Ending 7: Compromised Police Trap",
            "Ending 8: Failure Due to Lack of Clues (Normal)"
        ] if self.current_lang == "en" else [
            "Ending 1: Thân phận bị lật tẩy (GameOver)",
            "Ending 2: Ôm tiền trốn ra nước ngoài (Ẩn)",
            "Ending 3: Vua Cơm Tấm hoàn lương (Ẩn)",
            "Ending 4: Bị sát thủ thủ tiêu (Bad End)",
            "Ending 5: Sập bẫy do do dự phút cuối",
            "Ending 6: Bắt gọn Kiều Lương Tâm (True End)",
            "Ending 7: Sập bẫy Cảnh sát bị chiếm quyền",
            "Ending 8: Thất bại do thiếu manh mối (Normal)"
        ]
        statuses = ["UNLOCKED" if f"Ending {i}" in self.unlocked_endings else "🔒 Undiscovered" for i in range(1, 9)] if self.current_lang == "en" else ["ĐÃ MỞ KHÓA" if f"Ending {i}" in self.unlocked_endings else "🔒 Chưa khám phá" for i in range(1, 9)]
        
        text = f"TOTAL ENDINGS DISCOVERED: {len(self.unlocked_endings)}/8\n\n" if self.current_lang == "en" else f"TỔNG SỐ ENDING ĐÃ KHÁM PHÁ: {len(self.unlocked_endings)}/8\n\n"
        for i in range(8):
            text += f"{end_names[i]} -> [{statuses[i]}]\n"

        messagebox.showinfo("Endings", text)

    def start_night_0_tutorial(self):
        lessons = [
            ("Lesson 1: Service & Plate Assembly Process",
             "• Check customer's dish REQUEST on the interface.\n"
             "• Click ingredient buttons (Rice, Pork, Egg, Pork Roll, Skin) to make the correct dish.\n"
             "• Click 'SERVE DISH': Correct service earns money + reduces suspicion. Wrong service incurs a fine and increases suspicion!"),
            
            ("Lesson 2: Suspicion & Weather Management",
             "• Suspicion reaching 100% = Undercover identity exposed (GAME OVER)!\n"
             "• Each night features different weather (Rain, Blackout, Inspection...).\n"
             "• Purchase support items at the Late Night Shop to mitigate weather risks."),
            
            ("Lesson 3: Smuggled Package & Secret Compartment",
             "• Gang customers may bring a SMUGGLED PACKAGE to hide.\n"
             "• Click 'TAKE SMUGGLED' to store it in the under-table compartment and earn a fee.\n"
             "• Careful: If the compartment is full, the package spills, increasing Suspicion by +40%!"),

            ("Lesson 4: VIP Customers, Secret Fish Sauce & Shop Equipment",
             "• Upgrade Secret Fish Sauce through 3 levels ($150->$65, $200->$70, $300->$90) to increase income per serving.\n"
             "• Buy Wood Tables, Industrial Ceiling Fan & Steel Roller Door to boost revenue and safety."),

            ("Lesson 5: Mind Map & Achievement Badges",
             "• Open 'MIND MAP' during shifts to connect clues together, earn money & reduce Suspicion.\n"
             "• Unlock 6 prestigious Badge Achievements at the main menu."),

            ("Lesson 6: Collecting 10 Clues & Night 6 Showdown",
             "• Complete Daytime and Investigation tasks to collect all 10 Clues.\n"
             "• Night 6: Click 'SET TRAP' to surround and arrest boss Kieu Luong Tam.\n"
             "• The game features 8 rich Endings based on Money and Suspicion!")
        ] if self.current_lang == "en" else [
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
        tut_win.title("NIGHT 0 - COMPREHENSIVE TUTORIAL" if self.current_lang == "en" else "ĐÊM 0 - HUẤN LUYỆN TOÀN DIỆN GAMEPLAY")
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
            prefix = "🎓 NIGHT 0: TUTORIAL - " if self.current_lang == "en" else "🎓 ĐÊM 0: HUẤN LUYỆN - "
            lbl_title.config(text=f"{prefix}{title}")
            lbl_content.config(text=content)
            lbl_step.config(text=f"Lesson {idx + 1} / 6" if self.current_lang == "en" else f"Bài học {idx + 1} / 6")

            btn_prev.config(state="normal" if idx > 0 else "disabled")
            if idx == len(lessons) - 1:
                btn_next.config(text="FINISH (TO MENU)" if self.current_lang == "en" else "HOÀN THÀNH (VỀ MENU)", bg="#167c63")
            else:
                btn_next.config(text="NEXT ->" if self.current_lang == "en" else "BÀI TIẾP THEO ->", bg="#2b6cb0")

        def next_lesson():
            if current_idx[0] < len(lessons) - 1:
                current_idx[0] += 1
                update_lesson()
            else:
                tut_win.destroy()
                msg = "Completed Night 0 Tutorial! Ready for official operation." if self.current_lang == "en" else "Bạn đã hoàn thành Đêm 0 Huấn Luyện! Sẵn sàng bước vào chuyên án chính thức."
                messagebox.showinfo("Tutorial Completed" if self.current_lang == "en" else "Huấn luyện hoàn tất", msg, parent=self.root)

        def prev_lesson():
            if current_idx[0] > 0:
                current_idx[0] -= 1
                update_lesson()

        btn_prev = self.make_button(btn_frame, "<- PREV" if self.current_lang == "en" else "<- BÀI TRƯỚC", prev_lesson, width=15, bg="#3b4654")
        btn_prev.pack(side="left")

        btn_next = self.make_button(btn_frame, "NEXT ->" if self.current_lang == "en" else "BÀI TIẾP THEO ->", next_lesson, width=22, bg="#2b6cb0")
        btn_next.pack(side="right")

        update_lesson()

    def start_game(self):
        self.reset_game_data()
        self.game_running = True
        self.build_game_ui()

        intro_text = (
            "Fog blankets the small alley. Under your apron, you take on the 6-night campaign "
            "to dismantle Kieu Luong Tam's criminal syndicate.\n\n"
            "NEW FEATURES: Restaurant Equipment, MIND MAP and ACHIEVEMENT BADGES are ready!"
        ) if self.current_lang == "en" else (
            "Sương mù bao trùm con hẻm nhỏ. Dưới lớp tạp dề, bạn đảm nhận chiến dịch 6 đêm "
            "triệt phá đường dây tội phạm của Kiều Lương Tâm.\n\n"
            "TÍNH NĂNG MỚI : Trang bị Quán Cơm, SƠ ĐỒ TƯ DUY và hệ thống THÀNH TỰU HUY HIỆU đã sẵn sàng!"
        )
        messagebox.showinfo("Prologue" if self.current_lang == "en" else "Lời khởi đầu", intro_text)
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

        # Nút chuyển ngữ trên thanh tiêu đề game
        lang_txt = "🌐 VI" if self.current_lang == "en" else "🌐 EN"
        self.make_button(top_row, lang_txt, self.toggle_language, width=8, bg="#3b4654").pack(side="right", padx=5)

        self.lbl_stats = tk.Label(top_row, text="", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL)
        self.lbl_stats.pack(side="right", padx=5)

        self.lbl_weather_info = tk.Label(header, text="", font=("Segoe UI", 9, "italic"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_weather_info.pack(anchor="w", padx=15, pady=(0, 8))

        scene_box = tk.Frame(main, bg="#111318", highlightbackground=self.BORDER, highlightthickness=1)
        scene_box.pack(fill="x", pady=(0, 6))

        self.canvas_view = tk.Canvas(scene_box, height=160, bg="#111318", highlightthickness=0, bd=0)
        self.canvas_view.pack(fill="x", padx=8, pady=6)

        waiting_txt = "Waiting for customer..." if self.current_lang == "en" else "Đang chờ khách..."
        self.lbl_canvas_status = tk.Label(scene_box, text=waiting_txt, font=("Segoe UI", 11, "bold"), fg=self.GOLD, bg="#111318")
        self.lbl_canvas_status.pack(pady=(0, 8))

        dialog_box = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        dialog_box.pack(fill="x", pady=4)

        diag_title = "OPERATION PROGRESS & INTEL REPORTS" if self.current_lang == "en" else "DIỄN BIẾN CHUYÊN ÁN & TIN BÁO TÌNH BÁO"
        tk.Label(dialog_box, text=diag_title, font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL).pack(anchor="w", padx=12, pady=(6, 2))
        self.lbl_dialog = tk.Label(dialog_box, text="", font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL, wraplength=1000, justify="left", anchor="w")
        self.lbl_dialog.pack(fill="x", padx=12, pady=(0, 8))

        kitchen_title = " KITCHEN & UNDER-TABLE SECRET COMPARTMENT " if self.current_lang == "en" else " GÓC BẾP & KHOANG BÍ MẬT DƯỚI GẦM BÀN "
        self.kitchen_frame = tk.LabelFrame(
            main, text=kitchen_title, font=("Segoe UI", 10, "bold"),
            fg=self.GOLD, bg=self.PANEL2, padx=10, pady=8,
            highlightbackground=self.BORDER, highlightthickness=1, bd=0
        )
        self.kitchen_frame.pack(fill="x", pady=4)

        plate_row = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        plate_row.pack(fill="x", pady=(0, 4))

        plate_empty = "Current Plate: [Empty]" if self.current_lang == "en" else "Đĩa cơm đang làm: [Trống]"
        self.lbl_plate = tk.Label(plate_row, text=plate_empty, font=("Segoe UI", 10, "bold"), fg="#ffb454", bg=self.PANEL2)
        self.lbl_plate.pack(side="left")

        self.lbl_compartment = tk.Label(plate_row, text=f"Secret Comp: [0/{self.max_compartment}]", font=("Segoe UI", 10, "bold"), fg=self.RED, bg=self.PANEL2)
        self.lbl_compartment.pack(side="right")

        self.ing_frame = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        self.ing_frame.pack(fill="x", pady=(4, 0))

        ing_list = [("Rice", "Cơm"), ("Pork", "Sườn"), ("Egg", "Trứng"), ("Roll", "Chả"), ("Skin", "Bì")] if self.current_lang == "en" else [("Cơm", "Cơm"), ("Sườn", "Sườn"), ("Trứng", "Trứng"), ("Chả", "Chả"), ("Bì", "Bì")]
        for text, value in ing_list:
            btn = self.make_button(self.ing_frame, text, lambda item=value: self.add_ing(item), width=9)
            btn.pack(side="left", padx=2)

        reset_txt = "RESET" if self.current_lang == "en" else "LÀM LẠI"
        self.btn_reset_plate = self.make_button(self.ing_frame, reset_txt, self.reset_plate, width=9, bg="#9c3d3d")
        self.btn_reset_plate.pack(side="left", padx=(10, 2))

        serve_txt = "SERVE DISH" if self.current_lang == "en" else "PHỤC VỤ MÓN"
        self.btn_serve = self.make_button(self.ing_frame, serve_txt, self.serve_plate, width=14, bg="#248f57")
        self.btn_serve.pack(side="right", padx=2)

        actions = tk.Frame(main, bg=self.BG)
        actions.pack(fill="x", pady=(6, 0))

        t_btn = "TALK" if self.current_lang == "en" else "ĐỐI THOẠI"
        i_btn = "INVESTIGATE" if self.current_lang == "en" else "ĐIỀU TRA"
        m_btn = "MIND MAP" if self.current_lang == "en" else "SƠ ĐỒ TƯ DUY"
        s_btn = "TAKE PACKAGE" if self.current_lang == "en" else "NHẬN HÀNG NGẦM"
        a_btn = "SET TRAP" if self.current_lang == "en" else "GIĂNG BẪY"

        self.btn_talk = self.make_button(actions, t_btn, self.action_talk_customer, width=15, bg="#2b6cb0", height=2)
        self.btn_talk.pack(side="left", expand=True, fill="x", padx=(0, 2))

        self.btn_investigate = self.make_button(actions, i_btn, self.action_investigate, width=15, bg="#384454", height=2)
        self.btn_investigate.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_mindmap = self.make_button(actions, m_btn, self.open_mindmap_ui, width=16, bg="#d97706", height=2)
        self.btn_mindmap.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_smuggled_action = self.make_button(actions, s_btn, self.action_take_smuggled_package, width=16, bg="#805ad5", height=2, state="disabled")
        self.btn_smuggled_action.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_arrest = self.make_button(actions, a_btn, self.action_arrest, width=16, bg="#a63c3c", height=2)
        self.btn_arrest.pack(side="left", expand=True, fill="x", padx=(2, 0))

        bottom = tk.Frame(main, bg=self.BG)
        bottom.pack(fill="x", pady=(6, 0))
        menu_btn_txt = "TO MENU" if self.current_lang == "en" else "VỀ MENU"
        self.make_button(bottom, menu_btn_txt, self.confirm_back_menu, width=14, bg="#303743").pack(side="left")

        self.update_stats()
        self.root.after(50, self.draw_counter_scene)

    def open_mindmap_ui(self):
        mm_win = tk.Toplevel(self.root)
        mm_win.title("MIND MAP & EVIDENCE DEDUCTION" if self.current_lang == "en" else "SƠ ĐỒ TƯ DUY & SUY LUẬN BẰNG CHỨNG")
        mm_win.configure(bg=self.PANEL)
        mm_win.transient(self.root)
        mm_win.grab_set()
        self.center_window_dialog(mm_win, 780, 520)

        title_mm = "🧠 CASE MIND MAP DEDUCTION" if self.current_lang == "en" else "🧠 SƠ ĐỒ TƯ DUY CHUYÊN ÁN (MIND MAP DEDUCTION)"
        desc_mm = "Connect 2 corresponding clues to make important case deductions." if self.current_lang == "en" else "Ghép nối 2 manh mối tương ứng để đưa ra suy luận phá án quan trọng."

        tk.Label(mm_win, text=title_mm, font=("Segoe UI", 14, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(12, 4))
        tk.Label(mm_win, text=desc_mm, font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL).pack(pady=(0, 8))

        body = tk.Frame(mm_win, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=15, pady=5)

        left_title = " COLLECTED CLUES " if self.current_lang == "en" else " MANH MỐI ĐÃ THU THẬP "
        left_frame = tk.LabelFrame(body, text=left_title, font=("Segoe UI", 9, "bold"), fg=self.CYAN, bg=self.PANEL2, bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        listbox_clues = tk.Listbox(left_frame, bg=self.BG, fg=self.TEXT, font=("Segoe UI", 9), selectmode="multiple", highlightthickness=0, bd=0)
        listbox_clues.pack(fill="both", expand=True, padx=8, pady=8)

        for c in self.collected_clue_names:
            listbox_clues.insert("end", f"• {c}")

        right_title = " CONNECTION MAP & DEDUCTION " if self.current_lang == "en" else " SƠ ĐỒ KẾT NỐI & SUY LUẬN "
        right_frame = tk.LabelFrame(body, text=right_title, font=("Segoe UI", 9, "bold"), fg=self.GOLD, bg=self.PANEL2, bd=1)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        canvas = tk.Canvas(right_frame, bg="#111318", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=8, pady=8)

        def draw_mindmap():
            canvas.delete("all")
            cw = canvas.winfo_width() or 360
            ch = canvas.winfo_height() or 320
            cx, cy = cw // 2, ch // 2

            canvas.create_oval(cx - 55, cy - 25, cx + 55, cy + 25, fill="#9c3d3d", outline=self.GOLD, width=2)
            klt_label = "KIEU LUONG TAM\n(TARGET)" if self.current_lang == "en" else "KIỀU LƯƠNG TÂM\n(MỤC TIÊU)"
            canvas.create_text(cx, cy, text=klt_label, fill="white", font=("Segoe UI", 9, "bold"), justify="center")

            n = len(self.collected_clue_names)
            if n == 0:
                no_clue = "No clues yet!" if self.current_lang == "en" else "Chưa có manh mối nào!"
                canvas.create_text(cx, cy + 60, text=no_clue, fill=self.MUTED, font=("Segoe UI", 9, "italic"))
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
                w_msg = "Please select exactly 2 clues from the list to connect!" if self.current_lang == "en" else "Vui lòng chọn đúng 2 manh mối từ danh sách để thực hiện ghép nối!"
                messagebox.showwarning("Deduction" if self.current_lang == "en" else "Suy luận", w_msg, parent=mm_win)
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
                    al_msg = "You have already connected these 2 clues before!" if self.current_lang == "en" else "Bạn đã thực hiện ghép nối 2 manh mối này trước đó rồi!"
                    messagebox.showinfo("Already deduced" if self.current_lang == "en" else "Đã suy luận", al_msg, parent=mm_win)
                    return

                self.completed_deductions.add(rule_key)
                self.money += reward_m
                self.suspicion = max(0, self.suspicion + susp_red)
                self.deduction_count += 1

                succ_msg = (
                    f"💡 DISCOVERY: {result_title}\n\n"
                    f"• Funds reward: +${reward_m}\n"
                    f"• Suspicion reduced: {abs(susp_red)}%\n\n"
                    f"Case file progress advanced!"
                ) if self.current_lang == "en" else (
                    f"💡 PHÁT HIỆN: {result_title}\n\n"
                    f"• Kinh phí thưởng: +${reward_m}\n"
                    f"• Độ nghi ngờ giảm: {abs(susp_red)}%\n\n"
                    f"Tiến trình lập hồ sơ chuyên án đã tiến thêm một bước lớn!"
                )

                messagebox.showinfo("DEDUCTION SUCCESS!" if self.current_lang == "en" else "SUY LUẬN THÀNH CÔNG!", succ_msg, parent=mm_win)
                self.check_achievements()
                self.update_stats()
                mm_win.destroy()
            else:
                fail_msg = "These 2 clues do not form a logical link. Try another pair!" if self.current_lang == "en" else "2 manh mối này chưa tạo thành liên kết hợp lý. Hãy thử ghép cặp khác!"
                messagebox.showwarning("Connection failed" if self.current_lang == "en" else "Ghép nối thất bại", fail_msg, parent=mm_win)

        connect_btn = "CONNECT DEDUCTION" if self.current_lang == "en" else "GHÉP NỐI SUY LUẬN"
        close_btn = "CLOSE" if self.current_lang == "en" else "ĐÓNG"

        self.make_button(btn_bar, connect_btn, execute_deduction, width=22, bg="#248f57").pack(side="left", padx=5)
        self.make_button(btn_bar, close_btn, mm_win.destroy, width=14, bg="#3b4654").pack(side="right", padx=5)

    def trigger_informant_event(self):
        if self.informant_active or self.clues >= self.max_clues:
            return
        self.informant_active = True

        inf_win = tk.Toplevel(self.root)
        inf_win.title("EVENT: THE INFORMANT")
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

        i_title = "🕵️ INFORMANT APPEARS!" if self.current_lang == "en" else "🕵️ KẺ CHỈ ĐIỂM XUẤT HIỆN!"
        i_desc = "A mysterious visitor left a note with a secret code before disappearing!\nUnscramble the scrambled string before the paper self-destructs." if self.current_lang == "en" else "Một vị khách bí ẩn lén để lại mảnh giấy chứa mật mã rồi biến mất!\nGiải mã chuỗi ký tự đảo ngược trước khi tờ giấy tự hủy."

        tk.Label(inf_win, text=i_title, font=("Segoe UI", 14, "bold"), fg=self.RED, bg=self.PANEL).pack(pady=(15, 5))
        tk.Label(inf_win, text=i_desc, font=("Segoe UI", 9), fg=self.TEXT, bg=self.PANEL, justify="center").pack(pady=(0, 10))

        lbl_scrambled = tk.Label(inf_win, text=f"CODE:  {scrambled}", font=("Segoe UI", 16, "bold"), fg=self.GOLD, bg=self.PANEL2, relief="solid", bd=1, padx=15, pady=8)
        lbl_scrambled.pack(pady=5)

        lbl_timer = tk.Label(inf_win, text=f"⏱️ Time left: {self.informant_time_left}s", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL)
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
                to_msg = "The note was destroyed! You missed the clue." if self.current_lang == "en" else "Mảnh giấy đã bị tiêu hủy! Bạn bỏ lỡ cơ hội nhận Manh mối quý giá."
                messagebox.showwarning("Time's up!" if self.current_lang == "en" else "Hết giờ!", to_msg, parent=self.root)
            else:
                t_txt = f"⏱️ Time left: {self.informant_time_left}s" if self.current_lang == "en" else f"⏱️ Thời gian còn lại: {self.informant_time_left} giây"
                lbl_timer.config(text=t_txt)
                inf_win.after(1000, update_timer)

        def submit_answer(event=None):
            ans = entry_var.get().strip().upper()
            if ans.replace(" ", "") == target_word.replace(" ", ""):
                inf_win.destroy()
                self.informant_active = False
                new_clue = self.add_clue()
                msg = f"Decoded successfully!\nObtained valuable evidence:\n+ {new_clue}\n(Progress: {self.clues}/{self.max_clues})" if self.current_lang == "en" else f"Giải mã thành công!\nThu được vật chứng quý giá:\n+ {new_clue}\n(Tiến độ: {self.clues}/{self.max_clues})"
                messagebox.showinfo("Success" if self.current_lang == "en" else "Thành công", msg, parent=self.root)
                self.update_stats()
            else:
                err_msg = "Incorrect code! Try again quickly." if self.current_lang == "en" else "Mật mã chưa chính xác! Hãy thử lại nhanh lên."
                messagebox.showerror("Wrong code" if self.current_lang == "en" else "Mật mã sai", err_msg, parent=inf_win)
                entry_var.set("")

        entry.bind("<Return>", submit_answer)
        sub_btn_txt = "SUBMIT CODE" if self.current_lang == "en" else "XÁC NHẬN GIẢI MÃ"
        self.make_button(inf_win, sub_btn_txt, submit_answer, width=20, bg="#248f57").pack(pady=8)
        inf_win.after(1000, update_timer)

    def build_shop_ui(self):
        self.clear_root()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=40, pady=20)

        shop_title = "LATE NIGHT SHOP" if self.current_lang == "en" else "CỬA HÀNG ĐÊM MUỘN"
        tk.Label(outer, text=shop_title, font=("Segoe UI", 22, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(5, 2))
        
        sub_shop = f"CREATOR BY: Q-HOUSETEAM | Preparing Night {self.night} | Funds: ${self.money}" if self.current_lang == "en" else f"CREATOR BY: Q-HOUSETEAM | Chuẩn bị trước Đêm {self.night} | Vốn: ${self.money}"
        tk.Label(outer, text=sub_shop, font=("Segoe UI", 10), fg=self.CYAN, bg=self.BG).pack(pady=(0, 15))

        shop_card = tk.Frame(outer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        shop_card.pack(fill="both", expand=True, ipadx=10, ipady=5)

        recipe_name = "Secret Fish Sauce I" if self.current_lang == "en" else "Nước Mắm Bí Truyền I"
        recipe_desc = "Increases dish price from $45 to $65." if self.current_lang == "en" else "Tăng giá bán đĩa cơm từ $45 lên $65."
        recipe_cost = 150
        recipe_state = "normal"
        recipe_text = "BUY" if self.current_lang == "en" else "MUA"

        if self.recipe_level == 1:
            recipe_name = "Secret Fish Sauce II" if self.current_lang == "en" else "Nước Mắm Bí Truyền II"
            recipe_desc = "Increases dish price from $65 to $70." if self.current_lang == "en" else "Tăng giá bán đĩa cơm từ $65 lên $70."
            recipe_cost = 200
        elif self.recipe_level == 2:
            recipe_name = "Secret Fish Sauce III" if self.current_lang == "en" else "Nước Mắm Bí Truyền III"
            recipe_desc = "Increases dish price from $70 to $90 (Max)." if self.current_lang == "en" else "Tăng giá bán đĩa cơm từ $70 lên $90 (Tối đa)."
            recipe_cost = 300
        elif self.recipe_level >= 3:
            recipe_name = "Secret Fish Sauce (MAX)" if self.current_lang == "en" else "Nước Mắm Bí Truyền (MAX)"
            recipe_desc = "Max level reached ($90/dish)." if self.current_lang == "en" else "Đã đạt cấp tối đa ($90/đĩa cơm)."
            recipe_cost = 0
            recipe_state = "disabled"
            recipe_text = "MAXED" if self.current_lang == "en" else "ĐÃ MUA TỐI ĐA"

        items = [
            ("Premium Wood Tables", "+10% VIP customer rate and +$10 tip per dish.", 200, self.buy_wooden_tables, "has_wooden_tables"),
            ("Industrial Ceiling Fan", "Each correct service further reduces Suspicion by 2%.", 160, self.buy_ceiling_fan, "has_ceiling_fan"),
            ("Steel Roller Door", "Reduces 30% penalty suspicion on wrong dialogue/investigation.", 220, self.buy_iron_door, "has_iron_door"),
            ("Lucky Cat", "+35% VIP rate (10% -> 45%). Correct service +$25 tip.", 220, self.buy_meo_chieu_tai, "has_meo_chieu_tai"),
            ("VIP Broken Rice Sign", "+15% VIP customer appearance rate.", 180, self.buy_bien_hieu_vip, "has_bien_hieu_vip"),
            ("Special Kitchen Knife", "Correct service grants +$25 cooking skill tip.", 160, self.buy_special_knife, "has_special_knife"),
            ("Mini Speaker", "Enhances suspicion reduction when serving correctly.", 150, self.buy_speaker, "has_speaker"),
            ("Radio Walkie-Talkie Scanner", "Detects if police are compromised by gangs tonight.", 250, self.buy_radio_detector, "has_radio_detector"),
            ("Detective Magnifier", "Increases Informant timer to 45s & Investigation success to 80%.", 280, self.buy_magnifier, "has_magnifier"),
            ("Bulletproof Armor", "Saves your life once when Suspicion hits 100%.", 250, self.buy_armor, "has_armor"),
            ("High-Power Light Bulb", "Counters Blackout (Night 3) and reduces weather risks.", 120, self.buy_light, "has_light"),
            ("Underground Air Filter", "Clears fog, instantly reduces 15% Suspicion.", 180, self.buy_air_filter, "has_air_filter"),
            ("Mini Camouflage Camera", "Auto records, halves penalty when serving wrong dishes.", 220, self.buy_camera, "has_camera"),
            ("Compartment Expansion Kit", "Upgrades secret compartment capacity from 2 to 4 packages.", 180, self.buy_compartment_upgrade, "has_compartment_upgrade"),
            ("Mini Signal Jammer", "Prevents alarm. No suspicion increase if refusing smuggled packages.", 200, self.buy_jammer, "has_jammer"),
            ("Forged Documents", "Fools enemy scouts. Automatically reduces 10% Suspicion at start of night.", 200, self.buy_fake_docs, "has_fake_docs"),
            ("VIP Business License", "Counters Night 5 Inspector. Reduces all wrong-dish penalties by 50%.", 350, self.buy_vip_license, "has_vip_license"),
            ("Intel Radio Scanner", "High-tech. Instantly reveals 1 important clue when purchased.", 400, self.buy_radio_scanner, "has_radio_scanner"),
            ("Fake Audio Tape", "Dumps contraband on the Black Market at night WITHOUT increasing Suspicion.", 280, self.buy_fake_tape, "has_fake_tape")
        ] if self.current_lang == "en" else [
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
            btn_text = "BUY" if self.current_lang == "en" else "MUA"
            if getattr(self, key, False):
                btn_state, btn_text = "disabled", ("OWNED" if self.current_lang == "en" else "ĐÃ MUA")

            btn = self.make_button(row, btn_text, lambda c=cmd: c(), width=12, bg="#248f57", state=btn_state)
            btn.pack(side="right", padx=10)

        start_night_txt = f"START NIGHT {self.night} ->" if self.current_lang == "en" else f"BẮT ĐẦU ĐÊM {self.night} ->"
        btn_next = self.make_button(outer, start_night_txt, self.start_next_night, width=28, height=2, bg="#167c63")
        btn_next.pack(pady=10)

    def buy_wooden_tables(self):
        if self.money >= 200:
            self.money -= 200; self.has_wooden_tables = True
            msg = "Bought Wood Tables!\n+10% VIP rate & +$10 tip per dish." if self.current_lang == "en" else "Đã mua Bàn Ghế Gỗ Sưa!\nTăng 10% tỷ lệ Khách VIP và bo thêm $10 mỗi phần ăn."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_ceiling_fan(self):
        if self.money >= 160:
            self.money -= 160; self.has_ceiling_fan = True
            msg = "Installed Industrial Ceiling Fan!\nCorrect service reduces Suspicion by an extra 2%." if self.current_lang == "en" else "Đã lắp Quạt Trần Công Nghiệp!\nPhục vụ đúng món giúp giảm thêm 2% Độ nghi ngờ."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_iron_door(self):
        if self.money >= 220:
            self.money -= 220; self.has_iron_door = True
            msg = "Installed Steel Roller Door!\nReduces 30% Suspicion penalty on wrong dialogues." if self.current_lang == "en" else "Đã lắp Cửa Sắt Cuốn Cường Lực!\nGiảm 30% Độ nghi ngờ bị phạt khi chọn sai đối thoại."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_meo_chieu_tai(self):
        if self.money >= 220:
            self.money -= 220; self.has_meo_chieu_tai = True
            msg = "Bought Lucky Cat!\nVIP customer rate +35% and +$25 tip on correct service." if self.current_lang == "en" else "Đã mua Mèo Chiêu Tài!\nTỷ lệ Khách VIP tăng thêm +35% và bo thêm $25 khi phục vụ đúng món."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_bien_hieu_vip(self):
        if self.money >= 180:
            self.money -= 180; self.has_bien_hieu_vip = True
            msg = "Bought VIP Sign!\nVIP customer appearance rate +15%." if self.current_lang == "en" else "Đã mua Biển Hiệu Cơm Tấm VIP!\nTỷ lệ xuất hiện Khách VIP tăng thêm +15%."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_special_knife(self):
        if self.money >= 160:
            self.money -= 160; self.has_special_knife = True
            msg = "Bought Special Kitchen Knife!\nCorrect service grants +$25 tip." if self.current_lang == "en" else "Đã mua Dao Bếp Cao Cấp!\nPhục vụ đúng món được bo thêm $25."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_speaker(self):
        if self.money >= 150:
            self.money -= 150; self.has_speaker = True
            msg = "Bought Mini Speaker!\nIncreases suspicion reduction efficiency when serving correctly." if self.current_lang == "en" else "Đã mua Loa Quảng Cáo Mini!\nTăng hiệu quả giảm độ nghi ngờ khi phục vụ đúng món."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_radio_detector(self):
        if self.money >= 250:
            self.money -= 250; self.has_radio_detector = True
            msg = "Bought Radio Scanner!\nAlerts immediately if police are compromised tonight." if self.current_lang == "en" else "Đã mua Radio Rà Sóng!\nBáo động ngay nếu đêm nay Cảnh sát bị giăng bẫy ngược."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_light(self):
        if self.money >= 120: 
            self.money -= 120; self.has_light = True
            msg = "Bought High-power Light Bulb!\nNo longer fear Blackout on Night 3." if self.current_lang == "en" else "Đã mua Bóng đèn công suất lớn!\nKhông còn sợ sự cố cúp điện Đêm 3."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_recipe(self):
        if self.recipe_level == 0:
            if self.money >= 150:
                self.money -= 150
                self.recipe_level = 1
                self.serve_reward = 65
                msg = "Upgraded Secret Fish Sauce Lv 1!\nDish revenue increased from $45 -> $65." if self.current_lang == "en" else "Đã nâng cấp Nước Mắm Bí Truyền Cấp 1!\nDoanh thu đĩa cơm tăng từ $45 -> $65."
                messagebox.showinfo("Shop", msg)
                self.check_achievements()
                self.build_shop_ui()
            else:
                messagebox.showwarning("Shop", "Not enough $150 to upgrade!" if self.current_lang == "en" else "Bạn không đủ $150 để nâng cấp!")
        elif self.recipe_level == 1:
            if self.money >= 200:
                self.money -= 200
                self.recipe_level = 2
                self.serve_reward = 70
                msg = "Upgraded Secret Fish Sauce Lv 2!\nDish revenue increased from $65 -> $70." if self.current_lang == "en" else "Đã nâng cấp Nước Mắm Bí Truyền Cấp 2!\nDoanh thu đĩa cơm tăng từ $65 -> $70."
                messagebox.showinfo("Shop", msg)
                self.check_achievements()
                self.build_shop_ui()
            else:
                messagebox.showwarning("Shop", "Not enough $200 to upgrade!" if self.current_lang == "en" else "Bạn không đủ $200 để nâng cấp!")
        elif self.recipe_level == 2:
            if self.money >= 300:
                self.money -= 300
                self.recipe_level = 3
                self.serve_reward = 90
                msg = "Upgraded Secret Fish Sauce Lv 3 (MAX)!\nDish revenue increased from $70 -> $90." if self.current_lang == "en" else "Đã nâng cấp Nước Mắm Bí Truyền Cấp 3 (MAX)!\nDoanh thu đĩa cơm tăng từ $70 -> $90."
                messagebox.showinfo("Shop", msg)
                self.check_achievements()
                self.build_shop_ui()
            else:
                messagebox.showwarning("Shop", "Not enough $300 to upgrade!" if self.current_lang == "en" else "Bạn không đủ $300 để nâng cấp!")

    def buy_armor(self):
        if self.money >= 250: 
            self.money -= 250; self.has_armor = True; self.bought_armor_ever = True
            msg = "Bought Bulletproof Armor!\nProtects you 1 life when Suspicion hits 100%." if self.current_lang == "en" else "Đã mua Áo giáp chống đạn!\nBảo vệ bạn 1 mạng khi Nghi ngờ chạm 100%."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_air_filter(self):
        if self.money >= 180: 
            self.money -= 180; self.has_air_filter = True; self.suspicion = max(0, self.suspicion - 15)
            msg = "Bought Underground Air Filter!\nInstantly reduces 15% Suspicion." if self.current_lang == "en" else "Đã mua Máy lọc không khí ngầm!\nLập tức giảm 15% Độ nghi ngờ."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_camera(self):
        if self.money >= 220: 
            self.money -= 220; self.has_camera = True
            msg = "Installed Mini Camouflage Camera!\nHalves penalty when serving wrong dishes." if self.current_lang == "en" else "Đã lắp Camera ngụy trang mini!\nGiảm một nửa hình phạt khi phục vụ sai món."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_compartment_upgrade(self):
        if self.money >= 180:
            self.money -= 180; self.has_compartment_upgrade = True; self.max_compartment = 4
            msg = "Upgraded Secret Compartment!\nContraband capacity increased to 4 packages." if self.current_lang == "en" else "Đã nâng cấp Khoang bí mật!\nSức chứa tang vật tăng lên tối đa 4 gói."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_jammer(self):
        if self.money >= 200:
            self.money -= 200; self.has_jammer = True
            msg = "Equipped Mini Signal Jammer!\nSafe when refusing smuggled packages." if self.current_lang == "en" else "Đã trang bị Phá sóng mini!\nAn toàn tuyệt đối khi từ chối nhận hàng ngầm."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_fake_docs(self):
        if self.money >= 200:
            self.money -= 200; self.has_fake_docs = True
            msg = "Bought Forged Documents!\nAutomatically deducts 10% Suspicion at the start of each night." if self.current_lang == "en" else "Đã mua Tài liệu ngụy tạo!\nTự động trừ 10% Độ nghi ngờ ở đầu mỗi đêm."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_magnifier(self):
        if self.money >= 280:
            self.money -= 280; self.has_magnifier = True
            msg = "Bought Detective Magnifier!\nIncreases Informant decode time to 45s." if self.current_lang == "en" else "Đã mua Kính lúp thám tử!\nTăng thời gian giải mã Kẻ Chỉ Điểm lên 45s."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_vip_license(self):
        if self.money >= 350:
            self.money -= 350; self.has_vip_license = True
            msg = "Bought VIP Business License!\nAll wrong-dish penalties are now reduced by 50%!" if self.current_lang == "en" else "Đã mua Giấy phép kinh doanh VIP!\nGiờ đây mọi hình phạt khi sai món đều giảm 50%!"
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_radio_scanner(self):
        if self.money >= 400:
            if self.clues >= self.max_clues:
                messagebox.showwarning("Shop", "You already have all 10 clues, no need to buy this!" if self.current_lang == "en" else "Bạn đã có đủ 10 manh mối rồi, không cần thiết mua món này nữa!")
                return
            self.money -= 400; self.has_radio_scanner = True
            new_clue = self.add_clue()
            msg = f"Bought Radio Scanner!\nInstantly obtained important intel:\n+ {new_clue}" if self.current_lang == "en" else f"Đã mua Máy quét vô tuyến!\nLập tức thu được thông tin quan trọng:\n+ {new_clue}"
            messagebox.showinfo("High-tech Intel" if self.current_lang == "en" else "Tình báo cao cấp", msg)
            self.check_achievements()
            self.build_shop_ui()

    def buy_fake_tape(self):
        if self.money >= 280:
            self.money -= 280; self.has_fake_tape = True
            msg = "Bought Fake Audio Tape!\nNow you can dump black market items without fear of exposure." if self.current_lang == "en" else "Đã mua Băng ghi âm giả mạo!\nTừ giờ có thể tuồn hàng chợ đen mà không sợ bị lộ tẩy."
            messagebox.showinfo("Shop", msg)
            self.check_achievements()
            self.build_shop_ui()

    def start_next_night(self):
        if self.suspicion < 15:
            base_pressure = random.randint(15, 30)
            self.suspicion = max(self.suspicion, base_pressure)

        if self.night >= 3 and random.random() < 0.25:
            self.police_compromised = True
            if self.has_radio_detector:
                warn_msg = (
                    "⚠️ RADIO SCANNER ALERT\n"
                    "Signal detected: Police network tonight has been compromised by the syndicate!\n"
                    "DO NOT HAND OVER CONTRABAND TO POLICE TONIGHT!"
                ) if self.current_lang == "en" else (
                    "⚠️ BÁO ĐỘNG RADIO RÀ SÓNG\n"
                    "Tín hiệu rà sóng phát hiện: Mạng lưới Cảnh sát đêm nay đã bị băng nhóm chiếm quyền kiểm soát!\n"
                    "TUYỆT ĐỐI KHÔNG GIAO HÀNG NGẦM CHO CẢNH SÁT TRONG ĐÊM NAY!"
                )
                messagebox.showwarning("⚠️ RADIO ALERT", warn_msg)
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
            names_pool = ["Black-jacket henchman", "Gray-coat syndicate envoy", "Black Linh (Young assassin)"] if self.current_lang == "en" else ["Tên đàn em mặc áo đen", "Sứ giả băng nhóm áo khoác xám", "Lĩnh 'Den' (Sát thủ trẻ)"]
            dialogues_pool = [
                "Boss sent this contraband package, hide it well under the table. Don't let anyone see!",
                "Hot goods here, keep it for me until tomorrow morning. Good reward.",
                "I am Black Linh. Boss said to store this. Screw up and I'll make your night the brightest!"
            ] if self.current_lang == "en" else [
                "Boss gửi gói tang vật này, giấu kỹ dưới gầm bàn cho tao. Đừng để ai thấy!",
                "Hàng nóng đây, giữ hộ tao đến sáng mai. Có hậu tạ xứng đáng.",
                "Tao là Lĩnh 'Den'. Trùm bảo cất gói này. Làm không cẩn thận tao cho sáng nhất đêm!"
            ]
        else:
            names_pool = [
                "Sugarcane Granny (Hai)", "Shoeshine Boy (Bo)",
                "Lieutenant Nam (Local Police)", "Muddy coat man",
                "Scare-necked stranger", "Regular customer with heavy bag",
                "Hesitant youth with strange look", "Late night traveler"
            ] if self.current_lang == "en" else [
                "Bà Cụ Bán Nước Mía (Bà Hai)", "Cậu Bé Đánh Gi giày (Bé Bo)",
                "Thiếu Úy Nam (Công An Khu Vực)", "Gã đàn ông áo khoác dính bùn",
                "Kẻ lạ mặt có vết sẹo trên cổ", "Gã khách quen mang chiếc túi nặng",
                "Tên thanh niên ngập ngừng, ánh mắt lạ", "Hành khách di chuyển lúc đêm muộn"
            ]
            dialogues_pool = [
                "Grandpa Hai, I saw some tattooed guys lurking behind the alley...",
                "Mister, I found this paper with a code at the counter corner...",
                "Security has been quite complicated lately, watch out for strangers.",
                "Hurry up. I am in a big rush.",
                "I heard police are hunting Kieu Luong Tam very tightly.",
                "It's really cold tonight. Unusually quiet outside."
            ] if self.current_lang == "en" else [
                "Chú Hai ơi, tui thấy mấy thằng tay áo xăm xăm vừa rình mò sau hẻm đó...",
                "Chú ơi, con nhặt được tờ giấy chứa mã số này ở góc quầy...",
                "Tình hình an ninh dạo này khá phức tạp, anh bán cơm chú ý kẻ lạ nhé.",
                "Làm nhanh lên. Tao đang rất gấp.",
                "Nghe nói cảnh sát đang lùng Kiều Luong Tam rất gắt.",
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

        display_name = f"⭐ [VIP CUSTOMER] {raw_name}" if (self.current_lang == "en" and self.is_vip_customer) else (f"⭐ [KHÁCH VIP] {raw_name}" if self.is_vip_customer else raw_name)

        waiting_label = "Customer at counter: " if self.current_lang == "en" else "Khách trước quầy: "
        self.lbl_canvas_status.config(text=f"{waiting_label}{display_name}")
        req = ", ".join(self.current_plate_translated(self.current_customer["required"])) if self.current_lang == "en" else ", ".join(self.current_customer["required"])
        
        smuggler_note = ""
        if self.is_smuggler_customer:
            smuggler_note = "   |   ⚠️ [INCLUDES SMUGGLED PACKAGE]" if self.current_lang == "en" else "   |   ⚠️ [CÓ GÓI HÀNG NGẦM ĐÍNH KÈM]"
            self.btn_smuggled_action.config(state="normal", bg="#805ad5")
        else:
            self.btn_smuggled_action.config(state="disabled", bg="#384454")

        vip_note = "   |   ⭐ [VIP CUSTOMER TIP]" if (self.current_lang == "en" and self.is_vip_customer) else ("   |   ⭐ [KHÁCH VIP CÓ TIỀN BO]" if self.is_vip_customer else "")

        req_label = "DISH REQUEST" if self.current_lang == "en" else "YÊU CẦU MÓN"
        serving_lbl = "Serving" if self.current_lang == "en" else "Suất"

        self.lbl_dialog.config(
            text=f"[{display_name}]\n\"{self.current_customer['dialog']}\"\n\n"
                 f"{req_label}: [ {req} ]   |   {serving_lbl} {self.orders_completed_tonight + 1}/5{smuggler_note}{vip_note}"
        )
        self.update_plate_display()
        self.update_stats()
        self.draw_counter_scene()

    def current_plate_translated(self, reqs):
        trans = {"Cơm": "Rice", "Sườn": "Pork", "Trứng": "Egg", "Chả": "Roll", "Bì": "Skin"}
        return [trans.get(r, r) for r in reqs]

    def check_night_smuggler_dropoff(self):
        if len(self.hidden_compartment) > 0:
            count = len(self.hidden_compartment)
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Midnight Contraband Drop-off" if self.current_lang == "en" else "Điểm hẹn giao hàng ngầm lúc 00:00")
            dialog.configure(bg=self.PANEL)
            self.center_window_dialog(dialog, 580, 320)
            dialog.grab_set()

            h_title = f"YOU ARE HOLDING {count} CONTRABAND PACKAGES" if self.current_lang == "en" else f"BẠN ĐANG GIỮ {count} GÓI TANG VẬT"
            h_sub = "It's 00:00. How will you handle this contraband?" if self.current_lang == "en" else "Đã đến 00:00. Bạn sẽ xử lý số tang vật này như thế nào?"

            tk.Label(dialog, text=h_title, font=self.title_font, fg=self.RED, bg=self.PANEL).pack(pady=(20, 10))
            tk.Label(dialog, text=h_sub, font=self.bold_font, fg=self.TEXT, bg=self.PANEL).pack(pady=(0, 20))

            def choice_police():
                if self.police_compromised:
                    penalty_susp = count * 20 + 25
                    self.suspicion += penalty_susp
                    self.unlocked_endings.add("Ending 7")
                    self.save_endings()
                    self.check_achievements()
                    err_m = (
                        f"🚨 POLICE TRAP!\n"
                        f"Police station tonight was compromised by the syndicate!\n"
                        f"Contraband fell directly into the mole's hands. Boss suspects your identity!\n\n"
                        f"- Lost all contraband\n"
                        f"- Suspicion surged: +{penalty_susp}%"
                    ) if self.current_lang == "en" else (
                        f"🚨 BẪY NGƯỢC CẢNH SÁT!\n"
                        f"Đồn cảnh sát đêm nay đã bị băng nhóm chiếm quyền!\n"
                        f"Tang vật bạn chuyển qua đã lọt trực tiếp vào tay nội gián. Ông trùm bắt đầu nghi ngờ thân phận bạn!\n\n"
                        f"- Mất toàn bộ tang vật\n"
                        f"- Độ nghi ngờ tăng vọt: +{penalty_susp}%"
                    )
                    messagebox.showerror("🚨 POLICE TRAP", err_m)
                else:
                    bonus_money = count * 90
                    new_clue = self.add_clue()
                    self.money += bonus_money
                    msg = f"Handed over to team successfully!\n+ ${bonus_money} case funds" if self.current_lang == "en" else f"Tuồn cho đồng đội thành công!\n+ ${bonus_money} kinh phí chuyên án"
                    if new_clue:
                        msg += f"\n+ Evidence found: {new_clue}" if self.current_lang == "en" else f"\n+ Khui tang vật tìm thấy: {new_clue}"
                    messagebox.showinfo("Loyal" if self.current_lang == "en" else "Trung thành", msg)
                self.finish_dropoff(dialog)

            def choice_black_market():
                bonus_money = count * 250
                penalty_suspicion = count * 15
                
                if self.has_fake_tape:
                    penalty_suspicion = 0
                    msg = f"Sold on black market successfully!\n+ ${bonus_money} personal profit\n\n(Used Fake Tape: No Suspicion increase!)" if self.current_lang == "en" else f"Bán ra chợ đen trót lọt!\n+ ${bonus_money} lợi nhuận cá nhân\n\n(Dùng Băng ghi âm giả: Không bị tăng Độ nghi ngờ!)"
                else:
                    msg = f"Sold on black market successfully!\n+ ${bonus_money} personal profit\n- Increased {penalty_suspicion}% Suspicion!" if self.current_lang == "en" else f"Bán ra chợ đen trót lọt!\n+ ${bonus_money} lợi nhuận cá nhân\n- Tăng {penalty_suspicion}% Độ nghi ngờ từ hai phía!"
                    
                self.money += bonus_money
                self.suspicion += penalty_suspicion
                messagebox.showwarning("Corrupted" if self.current_lang == "en" else "Sa ngã", msg)
                self.finish_dropoff(dialog)

            btn_frame = tk.Frame(dialog, bg=self.PANEL)
            btn_frame.pack(fill="x", pady=10)
            
            b_pol = "HAND TO POLICE\n(Funds + Clue)" if self.current_lang == "en" else "GIAO CHO CẢNH SÁT\n(Kinh phí + Lấy Manh mối)"
            b_bm = "SELL BLACK MARKET\n(Much Money, High Suspicion)" if self.current_lang == "en" else "BÁN RA CHỢ ĐEN\n(Rất nhiều Tiền, Tăng nghi ngờ)"

            self.make_button(btn_frame, b_pol, choice_police, width=25, bg="#248f57", height=3).pack(side="left", padx=15)
            self.make_button(btn_frame, b_bm, choice_black_market, width=25, bg="#8f2424", height=3).pack(side="right", padx=15)
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
            messagebox.showinfo(f"ENDING: {title}", description)
        else:
            messagebox.showerror(f"ENDING: {title}", description)
            
        self.game_running = False
        self.build_main_menu()

    def trigger_next_day_logic(self):
        self.check_achievements()
        if self.night < 6:
            msg = f"Night {self.night} ended.\nMoving to next daytime mission." if self.current_lang == "en" else f"Đêm {self.night} kết thúc.\nChuyển sang nhiệm vụ ban ngày tiếp theo."
            messagebox.showinfo("Night Completed" if self.current_lang == "en" else "Hoàn thành ca đêm", msg)
            self.build_day_mission_ui(self.night)
        else:
            if self.clues >= 10:
                if self.suspicion >= 80:
                    self.trigger_ending("Ending 4", "ASSASINATED (BAD ENDING)", "Collected 10 clues but Suspicion was too high, exposing your identity. The syndicate sent an assassin to eliminate you before the operation!")
                else:
                    msg = "Survived 6 nights and collected all 10 clues! Ready to trap Kieu Luong Tam!" if self.current_lang == "en" else "Bạn đã sống sót qua 6 đêm và thu thập đủ 10 manh mối! Sẵn sàng giăng bẫy bắt Kiều Lương Tâm!"
                    messagebox.showinfo("6 Nights Completed" if self.current_lang == "en" else "Hoàn thành 6 đêm", msg)
                    self.update_stats()
            else:
                if self.money >= 1000:
                    self.trigger_ending("Ending 2", "ESCAPING ABROAD WITH MONEY (HIDDEN ENDING)", "Realizing arresting Kieu Luong Tam was too risky, you used your amassed fortune to book a flight to Dubai, living a luxurious life.")
                elif self.suspicion <= 25 and self.money >= 400:
                    self.trigger_ending("Ending 3", "REFORMED BROKEN RICE KING (HIDDEN ENDING)", "You retired from the police force, officially opening a famous Broken Rice restaurant chain, becoming a culinary legend.")
                elif self.suspicion >= 75:
                    self.trigger_ending("Ending 4", "ASSASINATED (BAD ENDING)", "High suspicion led Kieu Luong Tam to order his henchmen to clean up your restaurant in silence.")
                else:
                    clue_str = str(self.clues)
                    self.trigger_ending("Ending 8", "MISSION FAILED (NORMAL ENDING)", f"You survived 6 nights but only collected {clue_str}/10 clues. The operation was canceled, Kieu Luong Tam escaped.")

    def action_arrest(self):
        if not self.game_running:
            return

        if self.night < 6:
            messagebox.showwarning("Not ready" if self.current_lang == "en" else "Chưa đủ thời gian", "You must survive through 6 nights to gather the case file!" if self.current_lang == "en" else "Bạn phải bám trụ qua đủ 6 đêm để thu thập hồ sơ!")
            return

        if self.clues < 10:
            c_msg = f"You only have {self.clues}/10 clues. Need 10 clues to trap Kieu Luong Tam!" if self.current_lang == "en" else f"Bạn mới có {self.clues}/10 manh mối. Cần đủ 10 manh mối để giăng bẫy Kiều Lương Tâm!"
            messagebox.showerror("Not enough clues" if self.current_lang == "en" else "Chưa đủ manh mối", c_msg)
            return

        if not self.in_arrest_mode:
            self.in_arrest_mode = True
            self.arrest_step = 1
            self.kitchen_frame.pack_forget()
            self.btn_investigate.config(state="disabled")
            self.btn_talk.config(state="disabled")
            self.btn_smuggled_action.config(state="disabled")
            self.btn_mindmap.config(state="disabled")
            self.btn_arrest.config(text="CONTINUE RAID" if self.current_lang == "en" else "TIẾP TỤC VÂY BẮT", bg="#167c63")
            self.lbl_canvas_status.config(text="OPERATION: NIGHT 6 - FULL RAID")

        if self.arrest_step == 1:
            step1_txt = "[STEP 1: TASKFORCE ASSEMBLY]\n\nWith 10 valuable clues, the special taskforce has tightly surrounded Kieu Luong Tam's hideout." if self.current_lang == "en" else "[BƯỚC 1: HỘI QUÂN ĐẶC NHIỆM]\n\nVới đủ 10 manh mối đắt giá, lực lượng đặc nhiệm đã khép chặt vòng vây sào huyệt Kiều Lương Tâm."
            self.lbl_dialog.config(text=step1_txt)
            self.arrest_step = 2
        elif self.arrest_step == 2:
            step2_txt = "[STEP 2: ENTERING HIDEOUT]\n\nYou walk straight into the central office. Kieu Luong Tam is sitting waiting with a cold smile." if self.current_lang == "en" else "[BƯỚC 2: TIẾN VÀO SÀO HUYỆT]\n\nBạn bước thẳng vào phòng làm việc trung tâm. Kiều Lương Tâm đang ngồi chờ sẵn với nụ cười lạnh ngắt."
            self.lbl_dialog.config(text=step2_txt)
            self.arrest_step = 3
        elif self.arrest_step == 3:
            step3_txt = "[STEP 3: DIRECT CONFRONTATION]\n\nKIEU LUONG TAM: 'You thought you could outsmart me? Surrender and cooperate or end here.'" if self.current_lang == "en" else "[BƯỚC 3: ĐỐI ĐẦU TRỰC DIỆN]\n\nKIỀU LƯƠNG TÂM: 'Mày nghĩ qua mặt được tao sao? Hãy quy hàng hợp tác hoặc kết thúc tại đây.'"
            self.lbl_dialog.config(text=step3_txt)
            self.arrest_step = 4
        elif self.arrest_step == 4:
            q_title = "Fateful Choice (Night 6) - Q-HouseTeam"
            q_msg = "Will you signal the decisive assault or accept negotiation?" if self.current_lang == "en" else "Bạn sẽ phát tín hiệu tấn công quyết định hay chấp nhận thương lượng?"
            if messagebox.askyesno(q_title, q_msg):
                self.trigger_ending("Ending 6", "GLORIOUS VICTORY (TRUE ENDING)", "You order: 'Freeze, Police!' Special forces rush in and arrest Kieu Luong Tam!", is_win=True)
            else:
                self.trigger_ending("Ending 5", "TRAGIC ENDING (HESITATION TRAP)", "Last-minute hesitation made you fall into Kieu Luong Tam's trap and become a captive debtor.", is_win=False)

        self.draw_counter_scene()

    def check_game_over(self):
        if self.suspicion >= 100:
            if self.has_armor:
                self.has_armor = False
                self.suspicion = 60
                armor_msg = "Suspicion hit 100%! Bulletproof armor saved your life. Suspicion reduced to 60%." if self.current_lang == "en" else "Độ nghi ngờ chạm 100%! Áo giáp chống đạn giúp bạn thoát chết. Độ nghi ngờ giảm về 60%."
                messagebox.showwarning("Armor saved life" if self.current_lang == "en" else "Áo giáp cứu mạng", armor_msg)
                return False
            else:
                self.trigger_ending("Ending 1", "IDENTITY EXPOSED (GAME OVER)", "Suspicion reached 100%. Your undercover police identity was completely exposed!")
                return True
        return False

    def execute_day_mission(self, reward_money, reward_clue, susp_change):
        if reward_money < 0 and self.money < abs(reward_money):
            messagebox.showwarning("Not enough money" if self.current_lang == "en" else "Không đủ tiền", "You don't have enough funds for this paid plan!" if self.current_lang == "en" else "Bạn không đủ vốn để thực hiện phương án tốn phí này!")
            return

        self.money += reward_money
        clue_msg = ""
        if reward_clue > 0:
            for _ in range(reward_clue):
                new_c = self.add_clue()
                if new_c:
                    clue_msg += f"\n+ Evidence: {new_c}" if self.current_lang == "en" else f"\n+ Vật chứng: {new_c}"

        self.suspicion = max(0, min(100, self.suspicion + susp_change))
        msg = f"Daytime mission completed!\n\n• Financial change: ${reward_money}{clue_msg}\n• Suspicion change: {susp_change}%" if self.current_lang == "en" else f"Nhiệm vụ ban ngày hoàn tất!\n\n• Biến động tài chính: ${reward_money}{clue_msg}\n• Độ nghi ngờ thay đổi: {susp_change}%"
        messagebox.showinfo("Day Mission Result" if self.current_lang == "en" else "Kết quả nhiệm vụ ban ngày", msg)

        self.night += 1
        self.orders_completed_tonight = 0
        self.hour, self.minute = 20, 0
        self.check_achievements()
        self.build_shop_ui()

    def build_day_mission_ui(self, day):
        self.clear_root()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=40, pady=25)

        title_dm = f"DAYTIME - EXPANDED MISSION (MORNING AFTER NIGHT {day})" if self.current_lang == "en" else f"BAN NGÀY - NHIỆM VỤ MỞ RỘNG (SÁNG SAU ĐÊM {day})"
        tk.Label(outer, text=title_dm, font=("Segoe UI", 18, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(10, 2))
        tk.Label(outer, text="CREATOR BY: Q-HOUSETEAM | Careful undercover scouting choices.", font=("Segoe UI", 10), fg=self.CYAN, bg=self.BG).pack(pady=(0, 15))

        card = tk.Frame(outer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, ipadx=15, ipady=10)

        missions = {
            1: (
                "MISSION 1: SCOUTING WHOLESALE MARKET",
                "Spotted an unlabelled refrigerated truck unloading strange goods at dawn.",
                [
                    ("1. Stealthily record license plate & schedule", "Gather vehicle transport info.\n-> Reward +$60 funds & +1 Clue!", 60, 1, 0),
                    ("2. Approach driver directly", "Get quick info but easily noticed.\n-> Reward +$110 funds but +12% Suspicion.", 110, 0, 12),
                    ("3. Quietly retreat to ensure safety", "Maintain absolute identity safety.\n-> Reduce 10% Suspicion.", 0, 0, -10),
                    ("4. Bribe unloading area guard (Cost $20)", "Infiltrate restricted area.\n-> Gain +1 Clue and +$40, but cost fee.", -20, 1, 5)
                ] if self.current_lang == "en" else [
                    ("1. Lén lút ghi nhận biển số & lịch trình", "Thu thập thông tin phương tiện vận chuyển.\n-> Thưởng +$60 kinh phí & +1 Manh mối!", 60, 1, 0),
                    ("2. Tiếp cận dò hỏi trực tiếp tài xế", "Lấy thông tin nhanh nhưng dễ bị chú ý.\n-> Thưởng +$110 kinh phí nhưng tăng 12% Độ nghi ngờ.", 110, 0, 12),
                    ("3. Lặng lẽ rút lui bảo đảm an toàn", "Giữ vững thân phận an toàn tuyệt đối.\n-> Giảm 10% Độ nghi ngờ.", 0, 0, -10),
                    ("4. Hối lộ bảo vệ khu vực bốc dỡ (Tốn $20)", "Đột nhập sâu vào khu vực cấm.\n-> Nhận +1 Manh mối và +$40, nhưng tốn phí.", -20, 1, 5)
                ]
            ),
            2: (
                "MISSION 2: DECODING SECRET LETTER",
                "Obtained communication code from syndicate henchman: 'KLT-1082-WAREHOUSE'",
                [
                    ("1. Trace warehouse hideout coordinates", "Pinpoint crime gathering area.\n-> Gain +1 Clue!", 0, 1, 0),
                    ("2. Track black account transactions", "Freeze illegal financial source.\n-> Reward +$130 funds!", 130, 0, 0),
                    ("3. Spread fake rumors to cause chaos", "Mislead tracking forces.\n-> Strongly reduce 18% Suspicion.", 0, 0, -18),
                    ("4. Decode with specialized software (Cost $30)", "Gather high-tier info.\n-> Gain +1 Clue & Reward +$80!", 80, 1, 2)
                ] if self.current_lang == "en" else [
                    ("1. Truy vết tọa độ sào huyệt nhà kho", "Định vị khu vực tập kết tội phạm.\n-> Nhận ngay +1 Manh mối!", 0, 1, 0),
                    ("2. Theo dõi dòng tài khoản đen", "Phong tỏa nguồn tài chính bất hợp pháp.\n-> Thưởng +$130 kinh phí!", 130, 0, 0),
                    ("3. Tung tin đồn giả làm nhiễu loạn", "Đánh lạc hướng lực lượng theo dõi.\n-> Giảm mạnh 18% Độ nghi ngờ.", 0, 0, -18),
                    ("4. Giải mã bằng phần mềm chuyên dụng (Tốn $30)", "Thu thập thông tin cao cấp.\n-> Nhận ngay +1 Manh mối & Thưởng +$80!", 80, 1, 2)
                ]
            ),
            3: (
                "MISSION 3: APPROACHING SUPPLY BASE",
                "Discovered a sub-facility providing shady ingredients for Kieu Luong Tam's shop.",
                [
                    ("1. Infiltrate and collect transaction books", "Direct financial evidence.\n-> Gain +1 Clue and +$70!", 70, 1, 5),
                    ("2. Connect with internal warehouse staff", "Bribe mole for internal intel.\n-> Reward +$90 case funds.", 90, 0, 0),
                    ("3. Observe from afar to avoid detection", "Ensure absolute identity safety.\n-> Reduce 12% Suspicion.", 0, 0, -12),
                    ("4. Plant bug in warehouse (Cost $40)", "Monitor all syndicate movements.\n-> Gain +1 Clue and +$50!", 50, 1, 4)
                ] if self.current_lang == "en" else [
                    ("1. Đột nhập thu thập sổ sách giao dịch", "Thu thập bằng chứng tài chính trực tiếp.\n-> Nhận +1 Manh mối và +$70!", 70, 1, 5),
                    ("2. Móc nối với nhân viên kho bên trong", "Mua chuộc nội gián để lấy tin nội bộ.\n-> Thưởng +$90 kinh phí chuyên án.", 90, 0, 0),
                    ("3. Quan sát từ xa tránh bị phát hiện", "Giữ an toàn tuyệt đối cho thân phận.\n-> Giảm 12% Độ nghi ngờ.", 0, 0, -12),
                    ("4. Cài thiết bị nghe lén vào kho hàng (Tốn $40)", "Theo dõi toàn bộ động tĩnh băng nhóm.\n-> Nhận +1 Manh mối và +$50!", 50, 1, 4)
                ]
            ),
            4: (
                "MISSION 4: SUBURB WAREHOUSE INVESTIGATION",
                "Followed suspect to an old warehouse on the city outskirts.",
                [
                    ("1. Take documentary photos of suspicious activity", "Vivid records for case file.\n-> Gain +1 important Clue!", 0, 1, 0),
                    ("2. Lightly suppress guard for testimony", "Quick info via violence.\n-> Reward +$120 but +15% Suspicion.", 120, 0, 15),
                    ("3. Retreat to reinforce raid plan", "Maximum force preservation.\n-> Reduce 12% Suspicion.", 0, 0, -12),
                    ("4. Infiltrate server room to backup data (Cost $50)", "Get all criminal records.\n-> Gain +1 Clue & Reward +$90!", 90, 1, 8)
                ] if self.current_lang == "en" else [
                    ("1. Chụp ảnh tư liệu hoạt động đáng ngờ", "Tư liệu sống động cho hồ sơ.\n-> Nhận +1 Manh mối quan trọng!", 0, 1, 0),
                    ("2. Trấn áp nhẹ một tên lính canh lấy lời khai", "Thu thập thông tin nhanh chóng bằng bạo lực.\n-> Thưởng +$120 nhưng tăng 15% Độ nghi ngờ.", 120, 0, 15),
                    ("3. Rút lui củng cố kế hoạch vây bắt", "Bảo toàn lực lượng tối đa.\n-> Giảm 12% Độ nghi ngờ.", 0, 0, -12),
                    ("4. Đột nhập phòng máy chủ sao lưu dữ liệu (Tốn $50)", "Lấy toàn bộ hồ sơ tội phạm.\n-> Nhận +1 Manh mối & Thưởng +$90!", 90, 1, 8)
                ]
            ),
            5: (
                "MISSION 5: SHOWDOWN PREPARATION",
                "Final night before trapping the entire syndicate. Team on standby.",
                [
                    ("1. Review intelligence files", "Check file accuracy.\n-> Gain +1 final completion Clue!", 0, 1, 0),
                    ("2. Mobilize reserve case funds", "Ensure finances for taskforce.\n-> Reward +$180 large funds!", 180, 0, 0),
                    ("3. Check personal protective gear", "Maximum personal safety.\n-> Reduce 25% Suspicion.", 0, 0, -25),
                    ("4. Hold closed meeting with senior taskforce (Cost $60)", "Perfect raid plan.\n-> Gain +1 Clue & Reward +$100!", 100, 1, 5)
                ] if self.current_lang == "en" else [
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
            sel_btn_txt = "SELECT" if self.current_lang == "en" else "CHỌN"
            self.make_button(row, sel_btn_txt, cmd, width=10, bg="#2b6cb0").pack(side="right", padx=10)

    def action_talk_customer(self):
        if not self.game_running or not self.current_customer or self.in_arrest_mode:
            return
        if self.talked_current_customer:
            messagebox.showinfo("Dialogue", "You have already talked to this customer." if self.current_lang == "en" else "Bạn đã trò chuyện với vị khách này rồi.")
            return

        dialog_win = tk.Toplevel(self.root)
        dialog_win.title("Branching Dialogue Choice - Q-HouseTeam")
        dialog_win.configure(bg=self.PANEL)
        dialog_win.transient(self.root)
        dialog_win.grab_set()
        self.center_window_dialog(dialog_win, 600, 420)

        c_name = self.current_customer["name"]
        tk.Label(dialog_win, text=f"DIALOGUE: {c_name.upper()}", font=("Segoe UI", 13, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(15, 5))
        tk.Label(dialog_win, text=f"\"...{self.current_customer['dialog']}\"", font=("Segoe UI", 10, "italic"), fg=self.TEXT, bg=self.PANEL, wraplength=540).pack(pady=(0, 15))

        if "Sugarcane Granny" in c_name or "Bà Cụ Bán Nước Mía" in c_name:
            options = [
                ("1. Listen carefully", "Granny Hai shares lookout info.\n-> Reduce 10% Suspicion.", lambda: self.choose_dialogue(dialog_win, 101)),
                ("2. Buy a sugarcane juice ($10)", "Support granny.\n-> Reward +1 Clue!", lambda: self.choose_dialogue(dialog_win, 102)),
                ("3. Ignore and don't care", "Granny leaves shaking head.\n-> No change.", lambda: self.choose_dialogue(dialog_win, 103))
            ] if self.current_lang == "en" else [
                ("1. Lắng nghe dặn dò chu đáo", "Cụ Hai chia sẻ thông tin rình mò.\n-> Giảm 10% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 101)),
                ("2. Mua giúp cụ ly nước mía ($10)", "Ủng hộ cụ bớt vất vả.\n-> Thưởng +1 Manh mối từ cụ!", lambda: self.choose_dialogue(dialog_win, 102)),
                ("3. Lờ đi không quan tâm", "Cụ lắc đầu rời đi.\n-> Không thay đổi.", lambda: self.choose_dialogue(dialog_win, 103))
            ]
        elif "Shoeshine Boy" in c_name or "Cậu Bé Đánh Giày" in c_name:
            options = [
                ("1. Give boy a free broken rice plate", "Boy happily thanks you.\n-> Gives you a Clue paper!", lambda: self.choose_dialogue(dialog_win, 201)),
                ("2. Ask where he found the paper", "Bo points to bus station corner.\n-> Reduce 8% Suspicion.", lambda: self.choose_dialogue(dialog_win, 202)),
                ("3. Give some small change ($5)", "Boy wishes you good sales.\n-> Lucky +$15 reward.", lambda: self.choose_dialogue(dialog_win, 203))
            ] if self.current_lang == "en" else [
                ("1. Cho em bé ăn miễn phí đĩa cơm", "Em bé rối rít cảm ơn.\n-> Trao cho bạn mảnh giấy chứa Manh mối!", lambda: self.choose_dialogue(dialog_win, 201)),
                ("2. Hỏi xem em nhặt giấy ở đâu", "Bé Bo chỉ chỗ góc tối bến xe.\n-> Giảm 8% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 202)),
                ("3. Cho ít tiền lẻ ($5)", "Bé vui vẻ chúc chú bán đắt hàng.\n-> Thưởng +$15 may mắn.", lambda: self.choose_dialogue(dialog_win, 203))
            ]
        elif "Lieutenant Nam" in c_name or "Thiếu Úy Nam" in c_name:
            options = [
                ("1. Report good security situation", "Colleague leaves peacefully.\n-> Reduce 12% Suspicion.", lambda: self.choose_dialogue(dialog_win, 301)),
                ("2. Wink secret undercover signal", "Nam understands and shakes hands.\n-> Support secret +$50 funds.", lambda: self.choose_dialogue(dialog_win, 302)),
                ("3. Keep a hesitant attitude", "Nam suspiciously observes closely.\n-> Increase 10% Suspicion.", lambda: self.choose_dialogue(dialog_win, 303))
            ] if self.current_lang == "en" else [
                ("1. Báo cáo tình hình an ninh tốt", "Đồng nghiệp an tâm rời đi.\n-> Giảm 12% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 301)),
                ("2. Nháy ám hiệu trinh sát ngầm", "Thiếu úy Nam hiểu ý bắt tay.\n-> Hỗ trợ +$50 kinh phí secret.", lambda: self.choose_dialogue(dialog_win, 302)),
                ("3. Giữ thái độ lúng túng", "Thiếu úy nghi ngờ quan sát kỹ.\n-> Tăng 10% Độ nghi ngờ.", lambda: self.choose_dialogue(dialog_win, 303))
            ]
        else:
            options = [
                ("1. Friendly & Considerate", "Polite, gentle service.\n-> Reduce 5% Suspicion.", lambda: self.choose_dialogue(dialog_win, 1)),
                ("2. Subtle undercover inquiry", "Inquire about syndicate.\n-> 50% Clue | 50% Customer angered.", lambda: self.choose_dialogue(dialog_win, 2)),
                ("3. Use gang slang (Cost $15)", "Use underground slang.\n-> Strongly reduce 15% Suspicion.", lambda: self.choose_dialogue(dialog_win, 3))
            ] if self.current_lang == "en" else [
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

            sel_txt = "SELECT" if self.current_lang == "en" else "CHỌN"
            self.make_button(btn_frame, sel_txt, cmd, width=10, bg="#2b6cb0").pack(side="right", padx=10)

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
            msg = "You smiled and served. Customer is satisfied. (Suspicion -5%)" if self.current_lang == "en" else "Bạn mỉm cười phục vụ. Khách hàng tỏ ra hài lòng. (Độ nghi ngờ giảm 5%)"
        elif option == 2:
            if random.random() < 0.5:
                new_clue = self.add_clue()
                if new_clue:
                    msg = f"Customer accidentally revealed a valuable detail!\n\n(Obtained: {new_clue}! Total: {self.clues}/{self.max_clues})" if self.current_lang == "en" else f"Khách hàng vô tình hé lộ chi tiết đắt giá!\n\n(Thu được: {new_clue}! Tổng: {self.clues}/{self.max_clues})"
                else:
                    msg = "Customer chatted normally with no new info." if self.current_lang == "en" else "Khách hàng trò chuyện bình thường không có thông tin mới."
            else:
                p = self.apply_susp_penalty(15)
                msg = f"Inquiry was too obvious, customer is suspicious!\n\n(Suspicion increased +{p}%)" if self.current_lang == "en" else f"Lời dò hỏi quá lộ liễu khiến khách nghi ngờ!\n\n(Độ nghi ngờ tăng {p}%)"
        elif option == 3:
            if self.money >= 15:
                self.money -= 15
                self.suspicion = max(0, self.suspicion - 15)
                msg = "Used slang successfully. (Cost $15 - Suspicion reduced 15%)" if self.current_lang == "en" else "Dùng ám hiệu thành công. (Tốn $15 - Độ nghi ngờ giảm 15%)"
            else:
                msg = "Not enough money for slang ($15)." if self.current_lang == "en" else "Không đủ tiền thực hiện ám hiệu ($15)."
        elif option == 101:
            self.suspicion = max(0, self.suspicion - 10)
            msg = "Granny Hai warned you about gang members. (Suspicion -10%)" if self.current_lang == "en" else "Bà Hai nhắc nhở cẩn thận bọn xăm trổ. (Độ nghi ngờ giảm 10%)"
        elif option == 102:
            if self.money >= 10:
                self.money -= 10
                new_clue = self.add_clue()
                msg = f"Granny Hai touched and gave you a paper found at the station!\n\n(Obtained: {new_clue})" if self.current_lang == "en" else f"Cụ Hai cảm động đưa mảnh giấy nhặt được sau bến xe!\n\n(Thu được: {new_clue})"
            else:
                msg = "Not enough $10 for sugarcane juice." if self.current_lang == "en" else "Bạn không đủ $10 để mua nước mía."
        elif option == 103:
            msg = "Granny Hai quietly walked past." if self.current_lang == "en" else "Bà Hai lẳng lặng đi qua."
        elif option == 201:
            new_clue = self.add_clue()
            msg = f"Bo enjoyed the meal and handed over the code note!\n\n(Obtained: {new_clue})" if self.current_lang == "en" else f"Bé Bo ăn cơm ngon lành và trao tờ giấy ghi chép mật mã!\n\n(Thu được: {new_clue})"
        elif option == 202:
            self.suspicion = max(0, self.suspicion - 8)
            msg = "Bo pointed to the dark alley where henchmen gather. (Suspicion -8%)" if self.current_lang == "en" else "Bé Bo chỉ góc hẻm tối nơi tay sai tập kết. (Độ nghi ngờ giảm 8%)"
        elif option == 203:
            if self.money >= 5:
                self.money += 10
                msg = "Bo happily gave you a lucky coin! (+ $10)" if self.current_lang == "en" else "Bé Bo vui vẻ tặng bạn đồng xu may mắn! (+ $10)"
            else:
                msg = "Not enough $5." if self.current_lang == "en" else "Bạn không có đủ $5."
        elif option == 301:
            self.suspicion = max(0, self.suspicion - 12)
            msg = "Lieutenant Nam nodded and returned to station. (Suspicion -12%)" if self.current_lang == "en" else "Thiếu úy Nam gật đầu yên tâm quay về đồn. (Độ nghi ngờ giảm 12%)"
        elif option == 302:
            self.money += 50
            msg = "Lieutenant Nam secretly reinforced scouting funds. (+ $50)" if self.current_lang == "en" else "Thiếu úy Nam ngầm tiếp viện kinh phí trinh sát. (+ $50)"
        elif option == 303:
            p = self.apply_susp_penalty(10)
            msg = f"Hesitant attitude caught local police attention. (Suspicion +{p}%)" if self.current_lang == "en" else f"Thái độ lúng túng làm công an khu vực chú ý. (Độ nghi ngờ +{p}%)"

        res_title = "[DIALOGUE RESULT]" if self.current_lang == "en" else "[KẾT QUẢ ĐỐI THOẠI]"
        self.lbl_dialog.config(text=f"{res_title}\n\n{msg}")
        self.check_game_over()
        self.check_achievements()
        self.update_stats()

    def action_investigate(self):
        if not self.game_running or self.in_arrest_mode:
            return
        if self.clues >= self.max_clues:
            messagebox.showinfo("Clues" if self.current_lang == "en" else "Manh mối", f"You have collected all {self.max_clues} max clues." if self.current_lang == "en" else f"Bạn đã thu thập đủ tối đa {self.max_clues} manh mối.")
            return

        success_rate = 0.8 if getattr(self, "has_magnifier", False) else 0.5
        if random.random() < success_rate:
            new_clue = self.add_clue()
            if new_clue:
                msg = f"Successfully collected evidence:\n[{new_clue}]\n\nProgress: {self.clues}/{self.max_clues}" if self.current_lang == "en" else f"Thu thập thành công vật chứng:\n[{new_clue}]\n\nTiến độ: {self.clues}/{self.max_clues}"
                messagebox.showinfo("Evidence found" if self.current_lang == "en" else "Tìm thấy manh mối", msg)
        else:
            self.suspicion += 20
            msg = "Someone suspected your investigation action. Suspicion +20%." if self.current_lang == "en" else "Có kẻ nghi ngờ hành động điều tra của bạn. Độ nghi ngờ tăng 20%."
            messagebox.showwarning("Almost exposed" if self.current_lang == "en" else "Suýt bị lộ", msg)

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
            err_c = f"Secret compartment is full ({self.max_compartment}/{self.max_compartment})! Package spilled out, exposed to customer!\n\n(Suspicion +40%)" if self.current_lang == "en" else f"Khoang cất giấu đã đầy ({self.max_compartment}/{self.max_compartment})! Tang vật rơi ra ngoài khiến khách hàng phát hiện!\n\n(Độ nghi ngờ +40%)"
            messagebox.showerror("SECRET COMPARTMENT OVERLOAD!" if self.current_lang == "en" else "QUÁ TẢI KHOANG BÍ MẬT!", err_c)
            self.check_game_over()
            self.update_stats()
            return

        self.hidden_compartment.append("Illegal package")
        self.money += 40  
        self.is_smuggler_customer = False
        self.btn_smuggled_action.config(state="disabled", bg="#384454")
        
        suc_c = f"Secretly hid smuggled package in under-table compartment.\n• Earned: +$40 fee\n• Secret compartment: [{len(self.hidden_compartment)}/{self.max_compartment}]" if self.current_lang == "en" else f"Bạn đã lén giấu gói hàng ngầm vào khoang gầm bàn.\n• Nhận trước: +$40 tiền công\n• Khoang bí mật: [{len(self.hidden_compartment)}/{self.max_compartment}]"
        messagebox.showinfo("Successfully Stored" if self.current_lang == "en" else "Đã cất giấu thành công", suc_c)
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
            empty_p = "Current Plate: [Empty]" if self.current_lang == "en" else "Đĩa cơm đang làm: [Trống]"
            plate_prefix = "Current Plate: " if self.current_lang == "en" else "Đĩa cơm đang làm: "
            p_items = ", ".join(self.current_plate_translated(self.current_plate)) if self.current_lang == "en" else ", ".join(self.current_plate)
            self.lbl_plate.config(text=empty_p if not self.current_plate else f"{plate_prefix}[ {p_items} ]")
        if hasattr(self, "lbl_compartment"):
            comp_prefix = "Secret Comp: " if self.current_lang == "en" else "Khoang ngầm: "
            self.lbl_compartment.config(text=f"{comp_prefix}[{len(self.hidden_compartment)}/{self.max_compartment}]")

    def serve_plate(self):
        if not self.game_running or not self.current_customer or self.in_arrest_mode:
            return

        if self.is_smuggler_customer:
            if not self.has_jammer:
                self.suspicion += 10
                w_sm = "Ignored package and just served rice. Henchman glared and left. (Suspicion +10%)" if self.current_lang == "en" else "Bạn lờ đi gói hàng và chỉ phục vụ cơm. Tên đàn em lườm nguýt bỏ đi. (Độ nghi ngờ +10%)"
                messagebox.showwarning("Refused contraband" if self.current_lang == "en" else "Từ chối ngầm", w_sm)
            else:
                s_sm = "Thanks to Mini Signal Jammer, customer left quietly without alarming. (No suspicion increase)" if self.current_lang == "en" else "Nhờ có Thiết bị phá sóng mini, khách ngậm ngùi bỏ đi mà không thể báo động. (Không tăng nghi ngờ)"
                messagebox.showinfo("Safe refusal" if self.current_lang == "en" else "Từ chối an toàn", s_sm)
            self.is_smuggler_customer = False
            self.btn_smuggled_action.config(state="disabled", bg="#384454")

        required = self.current_customer["required"]
        if sorted(self.current_plate) == sorted(required):
            total_earned = self.serve_reward
            bonus_notes = []

            if self.has_special_knife:
                total_earned += 25
                bonus_notes.append("+$25 Special Knife" if self.current_lang == "en" else "+$25 Dao bếp cao cấp")

            if self.has_meo_chieu_tai:
                total_earned += 25
                bonus_notes.append("+$25 Lucky Cat" if self.current_lang == "en" else "+$25 Mèo chiêu tài")

            if getattr(self, "has_wooden_tables", False):
                total_earned += 10
                bonus_notes.append("+$10 Wood Tables" if self.current_lang == "en" else "+$10 Bàn ghế gỗ sưa")

            if self.is_vip_customer:
                vip_bonus = 35
                total_earned += vip_bonus
                bonus_notes.append(f"+${vip_bonus} VIP Tip" if self.current_lang == "en" else f"+${vip_bonus} Khách VIP bo")

            self.money += total_earned
            
            susp_reduce = 8 + (4 if self.has_speaker else 0) + (2 if getattr(self, "has_ceiling_fan", False) else 0)
            self.suspicion = max(0, self.suspicion - susp_reduce)
            
            self.orders_completed_tonight += 1
            self.advance_time()

            bonus_msg = f" ({', '.join(bonus_notes)})" if bonus_notes else ""
            suc_srv = f"Served correctly. Customer paid ${total_earned}{bonus_msg}." if self.current_lang == "en" else f"Phục vụ đúng món. Khách trả ${total_earned}{bonus_msg}."
            messagebox.showinfo("Success" if self.current_lang == "en" else "Thành công", suc_srv)
        else:
            self.money -= 10
            base_penalty = 40 if (self.night == 3 and not self.has_light) else 20
            susp_penalty = int(base_penalty * 0.5) if self.has_camera else base_penalty
            if self.has_vip_license:
                susp_penalty = susp_penalty // 2
                
            self.suspicion += susp_penalty
            self.advance_time()
            err_srv = f"Customer angered by wrong dish!\n(Suspicion penalty: +{susp_penalty}%)" if self.current_lang == "en" else f"Khách bực mình vì sai món!\n(Phạt Độ nghi ngờ: +{susp_penalty}%)"
            messagebox.showwarning("Wrong dish" if self.current_lang == "en" else "Sai món", err_srv)

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
        q_menu = "Are you sure you want to leave the operation? Progress will be lost." if self.current_lang == "en" else "Bạn có chắc muốn rời chuyên án? Tiến trình sẽ bị mất."
        if messagebox.askyesno("To Menu" if self.current_lang == "en" else "Về menu", q_menu):
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
        # English mapping fallback
        en_fallback = {
            "Sugarcane Granny (Hai)": visuals["Bà Cụ Bán Nước Mía (Bà Hai)"],
            "Shoeshine Boy (Bo)": visuals["Cậu Bé Đánh Giày (Bé Bo)"],
            "Lieutenant Nam (Local Police)": visuals["Thiếu Úy Nam (Công An Khu Vực)"],
            "Black Linh (Young assassin)": visuals["Lĩnh 'Đen' (Sát thủ trẻ)"],
            "Black-jacket henchman": visuals["Gã đàn ông áo khoác dính bùn"],
            "Gray-coat syndicate envoy": visuals["Kẻ lạ mặt có vết sẹo trên cổ"],
            "Muddy coat man": visuals["Gã đàn ông áo khoác dính bùn"],
            "Scare-necked stranger": visuals["Kẻ lạ mặt có vết sẹo trên cổ"],
            "Regular customer with heavy bag": visuals["Gã khách quen mang chiếc túi nặng"],
            "Hesitant youth with strange look": visuals["Tên thanh niên ngập ngừng, ánh mắt lạ"],
            "Late night traveler": visuals["Hành khách di chuyển lúc đêm muộn"]
        }
        all_dict = {**visuals, **en_fallback}
        return all_dict.get(name, visuals["Gã đàn ông áo khoác dính bùn"])

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
        canvas.create_text(cx, cy + 65, text="KIEU LUONG TAM", fill=self.RED, font=("Segoe UI", 10, "bold"))

    def update_stats(self):
        if hasattr(self, "lbl_stats"):
            weather_str = self.get_weather_name()
            time_lbl = "TIME" if self.current_lang == "en" else "GIỜ"
            night_lbl = "NIGHT" if self.current_lang == "en" else "ĐÊM"
            funds_lbl = "FUNDS" if self.current_lang == "en" else "VỐN"
            clues_lbl = "CLUES" if self.current_lang == "en" else "MANH MỐI"
            susp_lbl = "SUSPICION" if self.current_lang == "en" else "NGHI NGỜ"

            self.lbl_stats.config(
                text=f"{time_lbl}: {self.hour:02d}:{self.minute:02d}   |   "
                     f"{night_lbl} {self.night}/6 [{weather_str}]   |   {funds_lbl}: ${self.money}   |   "
                     f"{clues_lbl}: {self.clues}/{self.max_clues}   |   {susp_lbl}: {self.suspicion}%"
            )
        if hasattr(self, "lbl_weather_info"):
            w_prefix = "WEATHER: " if self.current_lang == "en" else "THỜI TIẾT: "
            self.lbl_weather_info.config(text=f"{w_prefix}{self.get_weather_description()}")
        if hasattr(self, "lbl_compartment"):
            comp_prefix = "Secret Comp: " if self.current_lang == "en" else "Khoang ngầm: "
            self.lbl_compartment.config(text=f"{comp_prefix}[{len(self.hidden_compartment)}/{self.max_compartment}]")

    def draw_counter_scene(self):
        if not hasattr(self, "canvas_view") or not self.canvas_view.winfo_exists():
            return

        self.canvas_view.delete("all")
        w = self.canvas_view.winfo_width() or 900
        h = self.canvas_view.winfo_height() or 160

        self.canvas_view.create_rectangle(0, 0, w, h, fill="#111318", outline="")
        self.canvas_view.create_rectangle(0, h - 30, w, h, fill="#1e232d", outline="#353c47", width=2)

        if self.in_arrest_mode:
            cx = w // 2
            cy = h // 2 - 10
            self.draw_klt_face(self.canvas_view, cx, cy)
        elif self.current_customer and self.customer_visual:
            cx = w // 2
            cy = h // 2 - 10
            self.draw_face(self.canvas_view, cx, cy, self.customer_visual, label=self.current_customer["name"], scale=1.1)

if __name__ == "__main__":
    root = tk.Tk()
    game = ComTam6NightsGame(root)
    root.mainloop()