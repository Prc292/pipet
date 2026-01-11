import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
PINK = (255, 182, 193)
ORANGE = (255, 165, 0)
BLUE = (100, 149, 237)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)

# Shop items database
SHOP_ITEMS = {
    'snacks': [
        {'id': 'cookie', 'name': 'Cookie', 'price': 5, 'hunger': 10, 'energy': 5, 'happiness': 5},
        {'id': 'candy', 'name': 'Candy', 'price': 3, 'hunger': 5, 'energy': 3, 'happiness': 10},
        {'id': 'chocolate', 'name': 'Chocolate', 'price': 8, 'hunger': 12, 'energy': 8, 'happiness': 15},
        {'id': 'lollipop', 'name': 'Lollipop', 'price': 4, 'hunger': 5, 'energy': 2, 'happiness': 8},
        {'id': 'donut', 'name': 'Donut', 'price': 7, 'hunger': 15, 'energy': 5, 'happiness': 12},
        {'id': 'ice_cream', 'name': 'Ice Cream', 'price': 10, 'hunger': 18, 'energy': 5, 'happiness': 20},
        {'id': 'popcorn', 'name': 'Popcorn', 'price': 6, 'hunger': 8, 'energy': 3, 'happiness': 7},
        {'id': 'chips', 'name': 'Chips', 'price': 5, 'hunger': 10, 'energy': 4, 'happiness': 6},
    ],
    'foods': [
        {'id': 'apple', 'name': 'Apple', 'price': 5, 'hunger': 15, 'energy': 8, 'health': 5},
        {'id': 'banana', 'name': 'Banana', 'price': 4, 'hunger': 12, 'energy': 10, 'health': 3},
        {'id': 'burger', 'name': 'Burger', 'price': 15, 'hunger': 35, 'energy': 15, 'happiness': 10},
        {'id': 'pizza', 'name': 'Pizza', 'price': 12, 'hunger': 30, 'energy': 12, 'happiness': 15},
        {'id': 'sandwich', 'name': 'Sandwich', 'price': 10, 'hunger': 25, 'energy': 10, 'health': 5},
        {'id': 'rice', 'name': 'Rice Bowl', 'price': 8, 'hunger': 20, 'energy': 12, 'health': 8},
        {'id': 'noodles', 'name': 'Noodles', 'price': 9, 'hunger': 22, 'energy': 10, 'happiness': 8},
        {'id': 'sushi', 'name': 'Sushi', 'price': 18, 'hunger': 28, 'energy': 15, 'health': 10},
    ],
    'drinks': [
        {'id': 'water', 'name': 'Water', 'price': 2, 'hunger': 5, 'energy': 3, 'health': 5},
        {'id': 'juice', 'name': 'Juice', 'price': 6, 'hunger': 10, 'energy': 8, 'happiness': 5},
        {'id': 'soda', 'name': 'Soda', 'price': 5, 'hunger': 8, 'energy': 5, 'happiness': 10},
        {'id': 'milk', 'name': 'Milk', 'price': 4, 'hunger': 12, 'energy': 5, 'health': 8},
        {'id': 'tea', 'name': 'Tea', 'price': 5, 'hunger': 5, 'energy': 10, 'health': 5},
        {'id': 'smoothie', 'name': 'Smoothie', 'price': 10, 'hunger': 15, 'energy': 12, 'health': 10},
    ],
    'energy': [
        {'id': 'energy_red', 'name': 'Red Bull', 'price': 15, 'hunger': 5, 'energy': 30, 'happiness': 5},
        {'id': 'energy_blue', 'name': 'Blue Energy', 'price': 15, 'hunger': 5, 'energy': 30, 'happiness': 5},
        {'id': 'energy_green', 'name': 'Green Power', 'price': 15, 'hunger': 5, 'energy': 30, 'happiness': 5},
        {'id': 'sports_drink', 'name': 'Sports Drink', 'price': 12, 'hunger': 8, 'energy': 25, 'health': 5},
        {'id': 'protein', 'name': 'Protein Shake', 'price': 18, 'hunger': 20, 'energy': 20, 'health': 10},
    ],
}

# Category info
CATEGORIES = [
    {'id': 'snacks', 'name': '🍪 Snacks', 'color': PINK},
    {'id': 'foods', 'name': '🍔 Foods', 'color': ORANGE},
    {'id': 'drinks', 'name': '🥤 Drinks', 'color': BLUE},
    {'id': 'energy', 'name': '⚡ Energy', 'color': GREEN},
]


class Button:
    def __init__(self, x, y, width, height, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False

    def draw(self, screen, font):
        color = tuple(min(c + 20, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)


class ItemCard:
    def __init__(self, item, x, y, width, height):
        self.item = item
        self.rect = pygame.Rect(x, y, width, height)
        self.buy_button = Button(x + 10, y + height - 40, width - 20, 30, 
                                 f"💰 {item['price']}", GREEN, WHITE)
        self.hover = False

    def draw(self, screen, font, small_font):
        # Card background
        color = LIGHT_GRAY if not self.hover else (250, 250, 250)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=10)

        # Icon placeholder (you'll replace this with actual images)
        icon_rect = pygame.Rect(self.rect.x + 30, self.rect.y + 10, 64, 64)
        pygame.draw.rect(screen, GRAY, icon_rect, border_radius=5)
        
        # Draw icon filename text
        icon_text = small_font.render(f"{self.item['id']}.png", True, DARK_GRAY)
        icon_text_rect = icon_text.get_rect(center=icon_rect.center)
        screen.blit(icon_text, icon_text_rect)

        # Item name
        name_surface = font.render(self.item['name'], True, BLACK)
        name_rect = name_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 80)
        screen.blit(name_surface, name_rect)

        # Stats
        y_offset = 105
        stats = []
        if 'hunger' in self.item and self.item['hunger']:
            stats.append(f"🍖 +{self.item['hunger']}")
        if 'energy' in self.item and self.item['energy']:
            stats.append(f"⚡ +{self.item['energy']}")
        if 'happiness' in self.item and self.item['happiness']:
            stats.append(f"😊 +{self.item['happiness']}")
        if 'health' in self.item and self.item['health']:
            stats.append(f"❤️ +{self.item['health']}")

        for stat in stats:
            stat_surface = small_font.render(stat, True, DARK_GRAY)
            stat_rect = stat_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + y_offset)
            screen.blit(stat_surface, stat_rect)
            y_offset += 18

        # Buy button
        self.buy_button.draw(screen, small_font)

    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        self.buy_button.update_hover(pos)

    def is_buy_clicked(self, pos):
        return self.buy_button.is_clicked(pos)


class TamagotchiShop:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tamagotchi Shop")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Game state
        self.coins = 100
        self.inventory = []
        self.message = "Welcome to the shop!"
        self.selected_category = 'snacks'
        
        # UI elements
        self.category_buttons = []
        self.item_cards = []
        self.scroll_offset = 0
        
        self.setup_ui()

    def setup_ui(self):
        # Category buttons
        button_width = 150
        button_height = 40
        start_x = 50
        for i, cat in enumerate(CATEGORIES):
            btn = Button(start_x + i * (button_width + 10), 120, 
                        button_width, button_height, cat['name'], cat['color'])
            btn.category_id = cat['id']
            self.category_buttons.append(btn)

        self.update_item_cards()

    def update_item_cards(self):
        self.item_cards = []
        items = SHOP_ITEMS[self.selected_category]
        
        card_width = 140
        card_height = 220
        cards_per_row = 4
        margin = 20
        start_x = 50
        start_y = 180

        for i, item in enumerate(items):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            
            card = ItemCard(item, x, y, card_width, card_height)
            self.item_cards.append(card)

    def buy_item(self, item):
        if self.coins >= item['price']:
            self.coins -= item['price']
            self.inventory.append(item)
            self.message = f"Bought {item['name']} for {item['price']} coins! 🎉"
        else:
            self.message = f"Not enough coins! Need {item['price'] - self.coins} more."

    def draw(self):
        # Background
        self.screen.fill((230, 230, 250))

        # Title
        title = self.title_font.render("🏪 Pet Shop", True, BLACK)
        self.screen.blit(title, (50, 30))

        # Coins display
        coins_bg = pygame.Rect(SCREEN_WIDTH - 200, 30, 150, 50)
        pygame.draw.rect(self.screen, YELLOW, coins_bg, border_radius=25)
        pygame.draw.rect(self.screen, BLACK, coins_bg, 3, border_radius=25)
        coins_text = self.font.render(f"💰 {self.coins}", True, BLACK)
        coins_rect = coins_text.get_rect(center=coins_bg.center)
        self.screen.blit(coins_text, coins_rect)

        # Message box
        msg_bg = pygame.Rect(50, 85, SCREEN_WIDTH - 100, 25)
        pygame.draw.rect(self.screen, (173, 216, 230), msg_bg, border_radius=5)
        pygame.draw.rect(self.screen, (70, 130, 180), msg_bg, 2, border_radius=5)
        msg_text = self.small_font.render(self.message, True, BLACK)
        msg_rect = msg_text.get_rect(center=msg_bg.center)
        self.screen.blit(msg_text, msg_rect)

        # Category buttons
        for btn in self.category_buttons:
            btn.draw(self.screen, self.font)

        # Item cards
        for card in self.item_cards:
            card.draw(self.screen, self.font, self.small_font)

        # Inventory
        inv_bg = pygame.Rect(50, SCREEN_HEIGHT - 80, SCREEN_WIDTH - 100, 70)
        pygame.draw.rect(self.screen, LIGHT_GRAY, inv_bg, border_radius=10)
        pygame.draw.rect(self.screen, DARK_GRAY, inv_bg, 2, border_radius=10)
        
        inv_title = self.font.render(f"🎒 Inventory ({len(self.inventory)} items)", True, BLACK)
        self.screen.blit(inv_title, (60, SCREEN_HEIGHT - 75))
        
        if not self.inventory:
            no_items = self.small_font.render("No items yet. Start shopping!", True, DARK_GRAY)
            self.screen.blit(no_items, (60, SCREEN_HEIGHT - 45))
        else:
            for i, item in enumerate(self.inventory[-10:]):  # Show last 10 items
                item_text = self.small_font.render(item['name'], True, BLACK)
                self.screen.blit(item_text, (60 + i * 70, SCREEN_HEIGHT - 45))

        pygame.display.flip()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Update hover states
        for btn in self.category_buttons:
            btn.update_hover(mouse_pos)
        for card in self.item_cards:
            card.update_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check category buttons
                for btn in self.category_buttons:
                    if btn.is_clicked(mouse_pos):
                        self.selected_category = btn.category_id
                        self.update_item_cards()
                        self.message = f"Browsing {btn.text}"

                # Check item buy buttons
                for card in self.item_cards:
                    if card.is_buy_clicked(mouse_pos):
                        self.buy_item(card.item)

        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# Run the shop
if __name__ == "__main__":
    shop = TamagotchiShop()
    shop.run()


"""
TO LOAD PNG IMAGES (once you have them):

1. Create an assets folder structure:
   assets/
       snacks/
           cookie.png
           candy.png
           ...
       foods/
           apple.png
           burger.png
           ...
       drinks/
           water.png
           ...
       energy/
           energy_red.png
           ...

2. Add this to the ItemCard class __init__:
   
   icon_path = f"assets/{category}/{item['id']}.png"
   try:
       self.icon = pygame.image.load(icon_path)
       self.icon = pygame.transform.scale(self.icon, (64, 64))
   except:
       self.icon = None

3. Replace the icon placeholder drawing code with:
   
   if self.icon:
       screen.blit(self.icon, icon_rect)
   else:
       pygame.draw.rect(screen, GRAY, icon_rect, border_radius=5)

"""