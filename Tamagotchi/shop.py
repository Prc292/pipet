import pygame

# === COLORS ===
DARK_BG = (45, 55, 72)
DARKER_BG = (26, 32, 44)
HEADER_BG = (74, 85, 104)
CONTENT_BG = (55, 65, 81)
LIGHT_BG = (247, 250, 252)
CARD_BG = (226, 232, 240)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
DARK_GOLD = (218, 165, 32)

PINK = (255, 182, 193)
ORANGE = (255, 165, 0)
BLUE = (66, 153, 225)
GREEN = (72, 187, 120)
GRAY = (203, 213, 224)
DARK_GRAY = (74, 85, 104)
BORDER_GRAY = (160, 174, 192)

SHOP_ITEMS = {
    'snacks': [
        {'id': 'cookie', 'name': 'Cookie', 'price': 5, 'emoji': '🍪', 'hunger': 10, 'energy': 5, 'happiness': 5},
        {'id': 'candy', 'name': 'Candy', 'price': 3, 'emoji': '🍬', 'hunger': 5, 'energy': 3, 'happiness': 10},
        {'id': 'chocolate', 'name': 'Chocolate', 'price': 8, 'emoji': '🍫', 'hunger': 12, 'energy': 8, 'happiness': 15},
        {'id': 'lollipop', 'name': 'Lollipop', 'price': 4, 'emoji': '🍭', 'hunger': 5, 'energy': 2, 'happiness': 8},
        {'id': 'donut', 'name': 'Donut', 'price': 7, 'emoji': '🍩', 'hunger': 15, 'energy': 5, 'happiness': 12},
        {'id': 'ice_cream', 'name': 'Ice Cream', 'price': 10, 'emoji': '🍦', 'hunger': 18, 'energy': 5, 'happiness': 20},
        {'id': 'popcorn', 'name': 'Popcorn', 'price': 6, 'emoji': '🍿', 'hunger': 8, 'energy': 3, 'happiness': 7},
        {'id': 'chips', 'name': 'Chips', 'price': 5, 'emoji': '🥔', 'hunger': 10, 'energy': 4, 'happiness': 6},
    ],
    'foods': [
        {'id': 'apple', 'name': 'Apple', 'price': 5, 'emoji': '🍎', 'hunger': 15, 'energy': 8, 'health': 5},
        {'id': 'banana', 'name': 'Banana', 'price': 4, 'emoji': '🍌', 'hunger': 12, 'energy': 10, 'health': 3},
        {'id': 'burger', 'name': 'Burger', 'price': 15, 'emoji': '🍔', 'hunger': 35, 'energy': 15, 'happiness': 10},
        {'id': 'pizza', 'name': 'Pizza', 'price': 12, 'emoji': '🍕', 'hunger': 30, 'energy': 12, 'happiness': 15},
        {'id': 'sandwich', 'name': 'Sandwich', 'price': 10, 'emoji': '🥪', 'hunger': 25, 'energy': 10, 'health': 5},
        {'id': 'rice', 'name': 'Rice Bowl', 'price': 8, 'emoji': '🍚', 'hunger': 20, 'energy': 12, 'health': 8},
        {'id': 'noodles', 'name': 'Noodles', 'price': 9, 'emoji': '🍜', 'hunger': 22, 'energy': 10, 'happiness': 8},
        {'id': 'sushi', 'name': 'Sushi', 'price': 18, 'emoji': '🍣', 'hunger': 28, 'energy': 15, 'health': 10},
    ],
    'drinks': [
        {'id': 'water', 'name': 'Water', 'price': 2, 'emoji': '💧', 'hunger': 5, 'energy': 3, 'health': 5},
        {'id': 'juice', 'name': 'Juice', 'price': 6, 'emoji': '🧃', 'hunger': 10, 'energy': 8, 'happiness': 5},
        {'id': 'soda', 'name': 'Soda', 'price': 5, 'emoji': '🥤', 'hunger': 8, 'energy': 5, 'happiness': 10},
        {'id': 'milk', 'name': 'Milk', 'price': 4, 'emoji': '🥛', 'hunger': 12, 'energy': 5, 'health': 8},
        {'id': 'tea', 'name': 'Tea', 'price': 5, 'emoji': '🍵', 'hunger': 5, 'energy': 10, 'health': 5},
        {'id': 'smoothie', 'name': 'Smoothie', 'price': 10, 'emoji': '🥤', 'hunger': 15, 'energy': 12, 'health': 10},
    ],
    'energy': [
        {'id': 'energy_red', 'name': 'Red Bull', 'price': 15, 'emoji': '⚡', 'hunger': 5, 'energy': 30, 'happiness': 5},
        {'id': 'energy_blue', 'name': 'Blue Energy', 'price': 15, 'emoji': '💙', 'hunger': 5, 'energy': 30, 'happiness': 5},
        {'id': 'energy_green', 'name': 'Green Power', 'price': 15, 'emoji': '💚', 'hunger': 5, 'energy': 30, 'happiness': 5},
        {'id': 'sports_drink', 'name': 'Sports Drink', 'price': 12, 'emoji': '🥤', 'hunger': 8, 'energy': 25, 'health': 5},
        {'id': 'protein', 'name': 'Protein Shake', 'price': 18, 'emoji': '🥤', 'hunger': 20, 'energy': 20, 'health': 10},
    ],
}

CATEGORIES = [
    {'id': 'snacks', 'name': '🍪 SNACKS', 'color': PINK},
    {'id': 'foods', 'name': '🍔 FOODS', 'color': ORANGE},
    {'id': 'drinks', 'name': '🥤 DRINKS', 'color': BLUE},
    {'id': 'energy', 'name': '⚡ ENERGY', 'color': GREEN},
]

class Button:
    def __init__(self, rect, text, color, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.base_color = color
        self.text_color = text_color
        self.hover = False

    def draw(self, screen, font):
        color = tuple(min(c + 20, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, DARKER_BG, self.rect, 2, border_radius=8)

        txt = font.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def update_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class ItemCard:
    def __init__(self, item, rect):
        self.item = item
        self.rect = pygame.Rect(rect)
        self.hover = False
        self.buy_btn = Button(
            (self.rect.x + 10, self.rect.bottom - 38, self.rect.width - 20, 28),
            f"Buy {item['price']}",
            GREEN
        )

    def draw(self, screen, font, small_font, emoji_font):
        # Card background
        bg = (250, 250, 250) if self.hover else LIGHT_BG
        pygame.draw.rect(screen, bg, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), border_radius=12)
        pygame.draw.rect(screen, BORDER_GRAY, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2, border_radius=12)

        # Item emoji
        e = emoji_font.render(self.item['emoji'], True, BLACK)
        screen.blit(e, (self.rect.x + self.rect.width // 2 - e.get_width() // 2, self.rect.y + int(self.rect.height * 0.05)))

        # Item name (slightly smaller)
        name = small_font.render(self.item['name'], True, BLACK)
        screen.blit(name, (self.rect.x + self.rect.width // 2 - name.get_width() // 2, self.rect.y + int(self.rect.height * 0.25)))

        # Buy button (taller and better aligned)
        self.buy_btn.rect.x = self.rect.x + int(self.rect.width * 0.05)
        self.buy_btn.rect.width = self.rect.width - int(self.rect.width * 0.1)
        self.buy_btn.rect.height = int(self.rect.height * 0.18)  # taller
        self.buy_btn.rect.y = self.rect.bottom - self.buy_btn.rect.height - int(self.rect.height * 0.02)
        self.buy_btn.draw(screen, small_font)

    def update_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.buy_btn.update_hover(mouse_pos)

    def buy_clicked(self, mouse_pos):
        return self.buy_btn.clicked(mouse_pos)


class ShopPanel:
    def __init__(self, panel_rect):
        self.panel_rect = pygame.Rect(panel_rect)
        self.width = self.panel_rect.width
        self.height = self.panel_rect.height

        # UI state
        self.selected_category = "snacks"
        self.scroll = 0
        self.max_scroll = 0

        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.emoji_font = pygame.font.Font(None, 40)

        # Buttons
        self.category_buttons = []
        self.back_button = Button(
            (self.panel_rect.x + self.panel_rect.width - 90, self.panel_rect.y + 10, 80, 30),
            "Close", DARK_GRAY
        )

        self.item_cards = []
        self.setup_category_buttons()
        self.update_items()

    def setup_category_buttons(self):
        x = self.panel_rect.x + int(self.width * 0.03)
        y = self.panel_rect.y + int(self.height * 0.07)
        w = int(self.width * 0.22)
        h = int(self.height * 0.08)
        gap = int(self.width * 0.015)

        self.category_buttons.clear()
        for cat in CATEGORIES:
            btn = Button((x, y, w, h), cat["name"], cat["color"])
            btn.category = cat["id"]
            self.category_buttons.append(btn)
            x += w + gap

    def update_items(self):
        self.item_cards = []
        list_y_start = self.panel_rect.y + int(self.height * 0.15)

        items = SHOP_ITEMS[self.selected_category]
        card_w = int(self.width * 0.22)
        card_h = int(self.height * 0.25)
        margin_x = int(self.width * 0.025)
        margin_y = int(self.height * 0.02)

        x_start = self.panel_rect.x + int((self.width - ((card_w + margin_x) * min(len(items), 4) - margin_x)) / 2)
        x = x_start
        y = list_y_start - self.scroll

        for item in items:
            card = ItemCard(item, (x, y, card_w, card_h))
            self.item_cards.append(card)
            x += card_w + margin_x
            if x + card_w > self.panel_rect.right - int(self.width * 0.03):
                x = x_start
                y += card_h + margin_y

        content_height = (y - (self.panel_rect.y + int(self.height * 0.15))) + card_h
        visible_height = self.height - int(self.height * 0.35)
        self.max_scroll = max(0, content_height - visible_height)

    def handle_events(self, events):
        mouse = pygame.mouse.get_pos()
        m_rel = (mouse[0], mouse[1])

        # Hover updates
        for btn in self.category_buttons:
            btn.update_hover(m_rel)
        self.back_button.update_hover(m_rel)
        for card in self.item_cards:
            card.update_hover(m_rel)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.clicked(m_rel):
                    return "close"

                # category switching
                for btn in self.category_buttons:
                    if btn.clicked(m_rel):
                        self.selected_category = btn.category
                        self.scroll = 0
                        self.update_items()
                        return

                # buying
                for card in self.item_cards:
                    if card.buy_clicked(m_rel):
                        return {"type": "buy", "item": card.item, "price": card.item["price"]}

            # scroll wheel
            if event.type == pygame.MOUSEWHEEL:
                self.scroll -= event.y * 30
                self.scroll = max(0, min(self.scroll, self.max_scroll))
                self.update_items()

        return None

    def draw(self, screen, offset_y=0):
        offset_x = int(self.width * 0.03)
        offset_y_internal = int(self.height * 0.05)

        # dim background
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # panel bg
        pygame.draw.rect(screen, DARK_BG, (self.panel_rect.x, self.panel_rect.y + offset_y, self.panel_rect.width, self.panel_rect.height), border_radius=12)
        pygame.draw.rect(screen, WHITE, (self.panel_rect.x, self.panel_rect.y + offset_y, self.panel_rect.width, self.panel_rect.height), 2, border_radius=12)

        # Title
        title = self.title_font.render("PET SHOP", True, GOLD)
        screen.blit(title, (self.panel_rect.x + offset_x, self.panel_rect.y + offset_y_internal + int(self.height * 0.02) + offset_y))

        # category buttons
        for btn in self.category_buttons:
            btn.draw(screen, self.font)

        # item cards
        clip = screen.get_clip()
        content_rect = pygame.Rect(
            self.panel_rect.x + offset_x,
            self.panel_rect.y + int(self.height * 0.15) + offset_y,
            self.width - 2 * offset_x,
            self.height - int(self.height * 0.25),
        )
        screen.set_clip(content_rect)

        for card in self.item_cards:
            card.draw(screen, self.font, self.small_font, self.emoji_font)

        screen.set_clip(clip)

        # close button
        self.back_button.rect.x = self.panel_rect.x + self.width - int(self.width * 0.15)
        self.back_button.rect.y = self.panel_rect.y + int(self.height * 0.02) + offset_y
        self.back_button.rect.width = int(self.width * 0.10)
        self.back_button.rect.height = int(self.height * 0.07)
        self.back_button.draw(screen, self.font)