from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Base, MenuItem, User, Review

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

session.query(MenuItem).delete()
session.commit()
session.query(Restaurant).delete()
session.commit()

# Create a dummy user1
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/'
                     '18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Menu for Urban Burger
restaurant1 = Restaurant(name="Urban Burger",
                         description="Lorem ipsum dolor sit amet, ei nam "
                                     "novum maiorum mnesarchum. "
                                     "An sed inermis accommodare, "
                                     "eos in dicant exerci tacimates.",
                         telephone="+23598746328", user_id=1)
session.add(restaurant1)
session.commit()

# French Fries menu item
menuItem1 = MenuItem(name="French Fries",
                     description="Lorem ipsum dolor sit amet, "
                                 "consectetuer adipiscing elit. "
                                 "Aenean commodo ligula eget dolor.",
                     category="Appetizer", price="$2.99",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem1)
session.commit()

# Chicken Burger menu item
menuItem2 = MenuItem(name="Chicken Burger",
                     description="Aenean massa. Cum sociis natoque "
                                 "penatibus et magnis dis parturient "
                                 "montes, nascetur ridiculus mus.",
                     category="Entree", price="$5.50",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem2)
session.commit()

# Chocolate Cake menu item
menuItem3 = MenuItem(name="Chocolate Cake",
                     description="Donec quam felis, ultricies nec, "
                                 "pellentesque eu, pretium quis, sem. "
                                 "Nulla consequat massa quis enim. "
                                 "Donec pede justo, fringilla vel.",
                     category="Dessert", price="$3.99",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem3)
session.commit()

# Sirloin Burger menu item
menuItem4 = MenuItem(name="Sirloin Burger",
                     description="In enim justo, rhoncus ut, imperdiet a, "
                                 "venenatis vitae, justo. Nullam dictum "
                                 "felis eu pede mollis pretium.",
                     category="Entree", price="$7.99",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem4)
session.commit()

# Root Beer menu item
menuItem5 = MenuItem(name="Root Beer",
                     description="Integer tincidunt. Cras dapibus. "
                                 "Vivamus elementum semper nisi. "
                                 "Aenean vulputate eleifend tellus.",
                     category="Beverage", price="$1.99",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem5)
session.commit()

# Iced Tea menu item
menuItem6 = MenuItem(name="Iced Tea",
                     description="Aenean leo ligula, porttitor eu, "
                                 "consequat vitae, eleifend ac, enim. "
                                 "Aliquam lorem ante, dapibus in, "
                                 "viverra quis, feugiat a, tellus.",
                     category="Beverage", price="$0.99",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem6)
session.commit()

# Grilled Cheese Sandwich menu item
menuItem7 = MenuItem(name="Grilled Cheese Sandwich",
                     description="On texas toast with American Cheese",
                     category="Entree", price="$3.49",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem7)
session.commit()

# Veggie Burger menu item
menuItem8 = MenuItem(name="Veggie Burger",
                     description="Phasellus viverra nulla ut "
                                 "metus varius laoreet. "
                                 "Quisque rutrum. Aenean imperdiet. "
                                 "Etiam ultricies nisi vel augue",
                     category="Entree", price="$5.99",
                     restaurant=restaurant1, user_id=1)
session.add(menuItem8)
session.commit()

# Create a dummy user2
User2 = User(name="Ahmed Khaled", email="ahmohllal@udacity.com",
             picture="http://books.davidemolin.com/"
                     "images/author/male/author-7.jpg")
session.add(User2)
session.commit()

# Menu for Super Stir Fry
restaurant2 = Restaurant(name="Super Stir Fry",
                         description="Ea dicat aliquip facilisis has, "
                                     "epicuri cotidieque te eam. "
                                     "Laudem voluptua in vis, "
                                     "ut eos dolores deseruisse,",
                         telephone="+98563325989", user_id=2)
session.add(restaurant2)
session.commit()

# Chicken Stir Fry menu item
menuItem1 = MenuItem(name="Chicken Stir Fry",
                     description="Curabitur ullamcorper ultricies nisi. "
                                 "Nam eget dui. Etiam rhoncus. ",
                     category="Entree", price="$7.99",
                     restaurant=restaurant2, user_id=2)
session.add(menuItem1)
session.commit()

# Peking Duck Fry menu item
menuItem2 = MenuItem(name="Peking Duck",
                     description="Maecenas tempus, "
                                 "tellus eget condimentum "
                                 "rhoncus, sem quam semper "
                                 "libero, sit amet "
                                 "adipiscing sem neque sed ipsum. ",
                     category="Entree", price="$25.75",
                     restaurant=restaurant2, user_id=2)
session.add(menuItem2)
session.commit()

# Spicy Tuna Roll menu item
menuItem3 = MenuItem(name="Spicy Tuna Roll",
                     description="Nam quam nunc, blandit vel, "
                                 "luctus pulvinar, hendrerit id, lorem. "
                                 "Maecenas nec odio et ante tincidunt tempus. "
                                 "Donec vitae sapien ut libero "
                                 "venenatis faucibus",
                     category="Entree", price="$15.50",
                     restaurant=restaurant2, user_id=2)
session.add(menuItem3)
session.commit()

# Nepali Momo menu item
menuItem4 = MenuItem(name="Nepali Momo",
                     description="Nullam quis ante. Etiam sit amet "
                                 "orci eget eros faucibus tincidunt.",
                     category="Entree", price="$12.25",
                     restaurant=restaurant2, user_id=2)
session.add(menuItem4)
session.commit()

# Beef Noodle Soup menu item
menuItem5 = MenuItem(name="Beef Noodle Soup",
                     description="uis leo. Sed fringilla mauris sit "
                                 "amet nibh. Donec sodales sagittis "
                                 "magna. Sed consequat, leo eget bibendum "
                                 "sodales, augue velit cursus nunc,",
                     category="Entree", price="$14.25",
                     restaurant=restaurant2, user_id=2)
session.add(menuItem5)
session.commit()

# Ramen menu item
menuItem6 = MenuItem(name="Ramen",
                     description="Li Europan lingues es membres "
                                 "del sam familie. Lor separat existentie "
                                 "es un myth. Por scientie, musica, "
                                 "sport etc, "
                                 "litot Europa usa li sam vocabular.",
                     category="Entree", price="$12.50",
                     restaurant=restaurant2, user_id=2)
session.add(menuItem6)
session.commit()

# Create a dummy user3
User3 = User(name="Angela Mircek", email="anreck@udacity.com",
             picture="http://www.morganstanley.com/"
                     "assets/images/people/tiles/diego-inigo-large.jpg")
session.add(User3)
session.commit()

# Menu for Panda Garden
restaurant3 = Restaurant(name="Panda Garden",
                         description="te mea duis tibique dissentiunt. "
                                     "Nominavi abhorreant eloquentiam ex nam",
                         telephone="+98666589899", user_id=3)
session.add(restaurant3)
session.commit()

# Pho menu item
menuItem1 = MenuItem(name="Pho",
                     description="A Vietnamese noodle soup "
                                 "consisting of broth, linguine-shaped "
                                 "rice noodles called banh pho, "
                                 "a few herbs, and meat.",
                     category="Entree", price="$8.99",
                     restaurant=restaurant3, user_id=3)
session.add(menuItem1)
session.commit()

# Chinese Dumplings menu item
menuItem2 = MenuItem(name="Chinese Dumplings",
                     description="A common Chinese dumpling "
                                 "which generally consists of "
                                 "minced meat and finely chopped "
                                 "vegetables wrapped into a "
                                 "piece of dough skin",
                     category="Appetizer", price="$6.99",
                     restaurant=restaurant3, user_id=3)

session.add(menuItem2)
session.commit()

# Gyoza menu item
menuItem3 = MenuItem(name="Gyoza",
                     description="The most prominent differences between "
                                 "Japanese-style gyoza and Chinese-style "
                                 "jiaozi are the rich garlic flavor, "
                                 "which is less noticeable in the "
                                 "Chinese version.",
                     category="Entree", price="$9.95",
                     restaurant=restaurant3, user_id=3)

session.add(menuItem3)
session.commit()

# Stinky Tofu menu item
menuItem4 = MenuItem(name="Stinky Tofu",
                     description="On refusa continuar payar custosi "
                                 "traductores. At solmen va esser necessi "
                                 "far uniform grammatica.",
                     category="Entree", price="$6.99",
                     restaurant=restaurant3, user_id=3)
session.add(menuItem4)
session.commit()

# Veggie Burger menu item
menuItem5 = MenuItem(name="Veggie Burger",
                     description="Li lingues differe "
                                 "solmen in li grammatica, "
                                 "li pronunciation e "
                                 "li plu commun vocabules. "
                                 "Omnicos directe al "
                                 "desirabilite de un nov lingua franca.",
                     category="Entree", price="$9.50",
                     restaurant=restaurant3, user_id=3)
session.add(menuItem5)
session.commit()


# Menu for Thyme for that
restaurant4 = Restaurant(name="Thyme for That Vegetarian Cuisine",
                         description="Pri ea populo invidunt, "
                                     "omnesque oportere "
                                     "vituperatoribus per eu, "
                                     "quo id zril docendi appellantur.",
                         telephone="+235478963201", user_id=3)

session.add(restaurant4)
session.commit()

# Tres Leches menu item
menuItem1 = MenuItem(name="Tres Leches",
                     description="Rich, luscious sponge cake soaked "
                                 "in sweet milk and topped with vanilla "
                                 "bean whipped cream and strawberries.",
                     category="Dessert", price="$2.99",
                     restaurant=restaurant4, user_id=3)
session.add(menuItem1)
session.commit()

# Mushroom Risotto menu item
menuItem2 = MenuItem(name="Mushroom Risotto",
                     description="it va esser Occidental. "
                                 "A un Angleso it va semblar un "
                                 "simplificat Angles, quam un skeptic.",
                     category="Entree", price="$5.99",
                     restaurant=restaurant4, user_id=3)
session.add(menuItem2)
session.commit()

# Honey Boba menu item
menuItem3 = MenuItem(name="Honey Boba",
                     description="Milk snow layered with honey boba, "
                                 "jasmine tea jelly, grass jelly, "
                                 "caramel, cream, and freshly made mochi.",
                     category="Dessert", price="$4.50",
                     restaurant=restaurant4, user_id=3)
session.add(menuItem3)
session.commit()

# Cauliflower Manchurian menu item
menuItem4 = MenuItem(name="Cauliflower Manchurian",
                     description="Li nov lingua franca va esser "
                                 "plu simplic e regulari quam li "
                                 "existent Europan lingues. "
                                 "It va esser tam simplic quam "
                                 "Occidental in fact.",
                     category="Appetizer", price="$6.95",
                     restaurant=restaurant4, user_id=3)
session.add(menuItem4)
session.commit()

# Aloo Gobi menu item
menuItem5 = MenuItem(name="Aloo Gobi",
                     description="Vegan goodness. "
                                 "Burrito filled with rice, "
                                 "garbanzo beans, "
                                 "curry sauce, potatoes (aloo), "
                                 "fried cauliflower (gobi) "
                                 "and chutney. Nom Nom",
                     category="Entree", price="$7.95",
                     restaurant=restaurant4, user_id=3)
session.add(menuItem5)
session.commit()

# Veggie Burger menu item
menuItem6 = MenuItem(name="Veggie Burger",
                     description="Pronunciation e plu sommun paroles. "
                                 "Ma quande lingues coalesce, li grammatica "
                                 "del resultant lingue es plu simplic e "
                                 "regulari quam ti del coalescent lingues.",
                     category="Entree", price="$6.80",
                     restaurant=restaurant4, user_id=3)
session.add(menuItem6)
session.commit()

# Create a dummy user4
User4 = User(name="Mohamed Khaled", email="mohmohllal@udacity.com",
             picture="https://organicthemes.com/demo/"
                     "profile/files/2012/12/profile_img.png")
session.add(User4)
session.commit()

# Menu for Tony's Bistro
restaurant5 = Restaurant(name="Tony\'s Bistro",
                         description="Cum eu erant tritani epicurei, "
                                     "at laoreet accumsan ponderum mea, "
                                     "in vulputate voluptatum "
                                     "theophrastus eum",
                         telephone="+96322214560", user_id=4)

session.add(restaurant5)
session.commit()

# Shellfish Tower menu item
menuItem1 = MenuItem(name="Shellfish Tower",
                     description="Lorem ipsum dolor sit amet, "
                                 "consectetuer adipiscing elit. "
                                 "Aenean commodo ligula eget dolor.",
                     category="Entree", price="$13.95",
                     restaurant=restaurant5, user_id=4)
session.add(menuItem1)
session.commit()

# Chicken and Rice menu item
menuItem2 = MenuItem(name="Chicken and Rice",
                     description="At solmen va esser necessi "
                                 "far uniform grammatica, "
                                 "pronunciation e plu sommun paroles.",
                     category="Entree", price="$4.95",
                     restaurant=restaurant5, user_id=4)
session.add(menuItem2)
session.commit()

# Mom's Spaghetti menu item
menuItem3 = MenuItem(name="Mom's Spaghetti",
                     description="Omnicos directe al desirabilite "
                                 "de un nov lingua franca: "
                                 "On refusa continuar payar "
                                 "custosi traductores.",
                     category="Entree", price="$6.95",
                     restaurant=restaurant5, user_id=4)
session.add(menuItem3)
session.commit()

# Choc Full menu item
menuItem4 = MenuItem(name="Choc Full",
                     description="Litot Europa usa li sam vocabular. "
                                 "Li lingues differe solmen in li grammatica. "
                                 "Li pronunciation e li plu commun vocabules.",
                     category="Dessert", price="$3.95",
                     restaurant=restaurant5, user_id=4)
session.add(menuItem4)
session.commit()

# Tonkatsu Ramen menu item
menuItem5 = MenuItem(name="Tonkatsu Ramen",
                     description="Cambridge amico dit me que Occidental es. "
                                 "Li Europan lingues es "
                                 "membres del sam familie. "
                                 "Lor separat existentie es un myth. "
                                 "Por scientie, musica, sport etc.",
                     category="Entree", price="$7.95",
                     restaurant=restaurant5, user_id=4)
session.add(menuItem5)
session.commit()


# Menu for Andala's
restaurant6 = Restaurant(name="Andala\'s",
                         description="Sea in nostro iriure interesset, "
                                     "movet paulo conclusionemque ei pro, "
                                     "maluisset scripserit disputando eos at.",
                         telephone="+20000102698", user_id=4)

session.add(restaurant6)
session.commit()


# Lamb Curry menu item
menuItem1 = MenuItem(name="Lamb Curry",
                     description="Slow cook that thang in a "
                                 "pool of tomatoes, onions "
                                 "and alllll those tasty "
                                 "Indian spices. Mmmm.",
                     category="Entree", price="$9.95",
                     restaurant=restaurant6, user_id=4)
session.add(menuItem1)
session.commit()

# Chicken Marsala menu item
menuItem2 = MenuItem(name="Chicken Marsala",
                     description="Donec pede justo, fringilla vel, "
                                 "aliquet nec, vulputate eget, arcu. "
                                 "In enim justo, rhoncus ut, imperdiet a, "
                                 "venenatis vitae, justo. ",
                     category="Entree", price="$7.95",
                     restaurant=restaurant6, user_id=4)
session.add(menuItem2)
session.commit()

# Potstickers menu item
menuItem3 = MenuItem(name="Potstickers",
                     description="Donec pede justo, fringilla vel, "
                                 "aliquet nec, vulputate eget, arcu. "
                                 "In enim justo, rhoncus ut, "
                                 "imperdiet a, venenatis vitae, justo. ",
                     category="Appetizer", price="$6.50",
                     restaurant=restaurant6, user_id=4)
session.add(menuItem3)
session.commit()

# Lamb Curry menu item
menuItem4 = MenuItem(name="Nigiri Sampler",
                     description="Aenean massa. "
                                 "Cum sociis natoque penatibus et "
                                 "magnis dis parturient montesd sdeirp "
                                 "dkmsiwc dkeoxc kekjviou cmdjehcdb.",
                     category="Appetizer", price="$6.75",
                     restaurant=restaurant6, user_id=4)
session.add(menuItem4)
session.commit()

# Veggie Burger menu item
menuItem5 = MenuItem(name="Veggie Burger",
                     description="Nascetur ridiculus mus. "
                                 "Donec quam felis, ultricies nec, "
                                 "pellentesque eu, pretium quis, sem. "
                                 "Nulla consequat massa quis enim.",
                     category="Entree", price="$7.00",
                     restaurant=restaurant6, user_id=4)
session.add(menuItem5)
session.commit()

# Create a dummy user5
User5 = User(name="Sondos Hamed", email="sondos@udacity.com",
             picture="http://www.penquin.co.za/wp-content/"
                     "uploads/2015/07/"
                     "emma-watson-black-and-white-profile.jpg")
session.add(User5)
session.commit()


# Menu for Auntie Ann's
restaurant7 = Restaurant(name="Auntie Ann\'s Diner'",
                         description="Euismod persequeris his id, "
                                     "agam indoctum ut eos. "
                                     "Mei error vocibus pertinax id.",
                         telephone="+986544454632", user_id=5)

session.add(restaurant7)
session.commit()

# Boysenberry Sorbet menu item
menuItem1 = MenuItem(name="Boysenberry Sorbet",
                     description="An unsettlingly huge amount of "
                                 "ripe berries turned into frozen "
                                 "(and seedless) awesomeness.",
                     category="Dessert", price="$2.99",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem1)
session.commit()

# Broiled salmon menu item
menuItem2 = MenuItem(name="Broiled salmon",
                     description="Nullam dictum felis "
                                 "eu pede mollis pretium. "
                                 "Integer tincidunt. "
                                 "Cras dapibus. "
                                 "Vivamus elementum semper nisi. "
                                 "Aenean vulputate eleifend tellus.",
                     category="Entree", price="$10.95",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem2)
session.commit()

# Morels menu item
menuItem3 = MenuItem(name="Morels",
                     description="Aenean leo ligula, porttitor eu, "
                                 "consequat vitae, eleifend ac, enim. "
                                 "Aliquam lorem ante, dapibus in, "
                                 "viverra quis, feugiat a, tellus",
                     category="Appetizer", price="$7.50",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem3)
session.commit()

# Tandoori Chicken menu item
menuItem4 = MenuItem(name="Tandoori Chicken",
                     description="Chicken marinated in "
                                 "yoghurt and seasoned with "
                                 "a spicy mix(chilli, tamarind "
                                 "among others) and slow cooked "
                                 "in a cylindrical clay or "
                                 "metal oven which gets its heat "
                                 "from burning charcoal.",
                     category="Entree", price="$8.95",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem4)
session.commit()

# Veggie Burger menu item
menuItem5 = MenuItem(name="Veggie Burger",
                     description="Quisque rutrum. Aenean imperdiet. "
                                 "Etiam ultricies nisi vel augue. "
                                 "Curabitur ullamcorper ultricies nisi. "
                                 "Nam eget dui. Etiam rhoncus.",
                     category="Entree", price="$9.50",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem5)
session.commit()

# Spinach Ice Cream menu item
menuItem6 = MenuItem(name="Spinach Ice Cream",
                     description="Maecenas tempus, tellus "
                                 "eget condimentum rhoncus, "
                                 "sem quam semper libero, "
                                 "sit amet adipiscing sem neque "
                                 "sed ipsum. Nam quam nunc.",
                     category="Dessert", price="$1.99",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem6)
session.commit()

# Chicken Fried Steak menu item
menuItem7 = MenuItem(name="Chicken Fried Steak",
                     description="Blandit vel, luctus pulvinar, "
                                 "hendrerit id, lorem. Maecenas nec "
                                 "odio et ante tincidunt tempus. "
                                 "Donec vitae sapien ut libero "
                                 "venenatis faucibus.",
                     category="Entree", price="$8.99",
                     restaurant=restaurant7, user_id=5)
session.add(menuItem7)
session.commit()

# Menu for Cocina Y Amor
restaurant8 = Restaurant(name="Cocina Y Amor",
                         description="Sumo propriae periculis ad mel, "
                                     "stet mediocrem corrumpit mel te. "
                                     "Id labore detracto delectus pri, "
                                     "dolor ponderum sit id. "
                                     "Ex noster rationibus pri. "
                                     "Has dicat ancillae.",
                         telephone="+98653214789", user_id=5)

session.add(restaurant8)
session.commit()

# Super Burrito menu item
menuItem1 = MenuItem(name="Super Burrito",
                     description="Marinated Pork, Rice, "
                                 "Beans, Avocado, Cilantro, "
                                 "Salsa, Tortilla",
                     category="Entree", price="$5.95",
                     restaurant=restaurant8, user_id=5)
session.add(menuItem1)
session.commit()

# Cachapa menu item
menuItem2 = MenuItem(name="Cachapa",
                     description="Golden brown, "
                                 "corn-based Venezuelan pancake; "
                                 "usually stuffed with queso telita "
                                 "or queso de mano, "
                                 "and possibly lechon.",
                     category="Entree", price="$7.99",
                     restaurant=restaurant8, user_id=5)
session.add(menuItem2)
session.commit()


restaurant9 = Restaurant(name="State Bird Provisions",
                         description="Eos falli vituperatoribus an, "
                                     "pro te viris discere. "
                                     "Cu mel malis sanctus, "
                                     "illum propriae pri eu.Sea eu "
                                     "nulla albucius platonem, "
                                     "pro cu tibique intellegam, ne "
                                     "veri ponderum vix. "
                                     "Duo an libris mucius moderatius,",
                         telephone="+52140023657", user_id=5)

session.add(restaurant9)
session.commit()

# Chantrelle Toast menu item
menuItem1 = MenuItem(name="Chantrelle Toast",
                     description="Crispy Toast with Sesame Seeae "
                                 "vitae dicta sunt explicabo. "
                                 "Nemo enim ipsam voluptatemds "
                                 "slathered with buttery "
                                 "chantrelle mushrooms.",
                     category="Appetizer", price="$5.95",
                     restaurant=restaurant9, user_id=5)
session.add(menuItem1)
session.commit()

# Guanciale Chawanmushi menu item
menuItem2 = MenuItem(name="Guanciale Chawanmushi",
                     description="Sed ut perspiciatis unde omnis iste "
                                 "natus error sit voluptatem accusantium "
                                 "doloremque laudantium, totam rem aperiam.",
                     category="Dessert", price="$6.95",
                     restaurant=restaurant9, user_id=5)
session.add(menuItem2)
session.commit()

# Lemon Curd menu item
menuItem3 = MenuItem(name="Lemon Curd",
                     description="Ullam quis ante. Etiam sit amet orci "
                                 "eget eros faucibus tincidunt. "
                                 "Duis leo. Sed fringilla mauris "
                                 "sit amet nibh. Donec sodales "
                                 "sagittis magna.",
                     category="Dessert", price="$4.25",
                     restaurant=restaurant9, user_id=5)
session.add(menuItem3)
session.commit()

# Create a dummy review1
review1 = Review(rate=3,
                 content="Lorem ipsum dolor sit amet, "
                         "consectetuer adipiscing elit. "
                         "Aenean commodo ligula eget dolor.",
                 menuItem_id=1, user_id=1)
session.add(review1)
session.commit()

# Create a dummy review2
review2 = Review(rate=4,
                 content="Metus condimentum sodales suspendisse "
                         "justo, quis dolor id wisi pellentesque, "
                         "nostra nunc fusce mi.",
                 menuItem_id=1, user_id=2)
session.add(review2)
session.commit()


# Create a dummy review3
review3 = Review(rate=2,
                 content="Porta vitae orci aliquam, "
                         "faucibus massa consectetuer viverra erat. "
                         "Tellus elit ut in, nunc auctor dapibus sed enim.",
                 menuItem_id=1, user_id=3)
session.add(review3)
session.commit()

# Create a dummy review4
review4 = Review(rate=3,
                 content="Lorem ante vitae maecenas arcu, "
                         "ornare nonummy vitae amet sapien. "
                         "Eu quam dui aliquam, "
                         "ac vitae sit lacus tincidunt.",
                 menuItem_id=1, user_id=4)
session.add(review4)
session.commit()

# Create a dummy review5
review5 = Review(rate=5,
                 content="Lorem ipsum dolor sit amet, "
                         "consectetuer adipiscing elit. "
                         "Aenean commodo ligula eget dolor.",
                 menuItem_id=2, user_id=1)
session.add(review5)
session.commit()

# Create a dummy review6
review6 = Review(rate=5,
                 content="Metus condimentum sodales suspendisse "
                         "justo, quis dolor id wisi pellentesque, "
                         "nostra nunc fusce mi.",
                 menuItem_id=2, user_id=2)
session.add(review6)
session.commit()


# Create a dummy review7
review7 = Review(rate=4,
                 content="Porta vitae orci aliquam, "
                         "faucibus massa consectetuer viverra erat. "
                         "Tellus elit ut in, nunc auctor dapibus sed enim.",
                 menuItem_id=5, user_id=3)
session.add(review7)
session.commit()

# Create a dummy review8
review8 = Review(rate=3,
                 content="Lorem ante vitae maecenas arcu, "
                         "ornare nonummy vitae amet sapien. "
                         "Eu quam dui aliquam, "
                         "ac vitae sit lacus tincidunt.",
                 menuItem_id=5, user_id=4)
session.add(review8)
session.commit()

# Create a dummy review9
review9 = Review(rate=5,
                 content="Lorem ipsum dolor sit amet, "
                         "consectetuer adipiscing elit. "
                         "Aenean commodo ligula eget dolor.",
                 menuItem_id=7, user_id=1)
session.add(review9)
session.commit()

# Create a dummy review10
review10 = Review(rate=4,
                  content="Metus condimentum sodales suspendisse "
                          "justo, quis dolor id wisi pellentesque, "
                          "nostra nunc fusce mi.",
                  menuItem_id=2, user_id=3)
session.add(review10)
session.commit()


# Create a dummy review11
review11 = Review(rate=3,
                  content="Porta vitae orci aliquam, "
                          "faucibus massa consectetuer viverra erat. "
                          "Tellus elit ut in, nunc auctor dapibus sed enim.",
                  menuItem_id=6, user_id=2)
session.add(review11)
session.commit()

# Create a dummy review12
review12 = Review(rate=5,
                  content="Lorem ante vitae maecenas arcu, "
                          "ornare nonummy vitae amet sapien. "
                          "Eu quam dui aliquam, "
                          "ac vitae sit lacus tincidunt.",
                  menuItem_id=7, user_id=3)
session.add(review12)
session.commit()

# Create a dummy review13
review13 = Review(rate=5,
                  content="Lorem ipsum dolor sit amet, "
                          "consectetuer adipiscing elit. "
                          "Aenean commodo ligula eget dolor.",
                  menuItem_id=19, user_id=1)
session.add(review13)
session.commit()

# Create a dummy review14
review14 = Review(rate=4,
                  content="Metus condimentum sodales suspendisse "
                          "justo, quis dolor id wisi pellentesque, "
                          "nostra nunc fusce mi.",
                  menuItem_id=10, user_id=2)
session.add(review14)
session.commit()


# Create a dummy review15
review15 = Review(rate=3,
                  content="Porta vitae orci aliquam, "
                          "faucibus massa consectetuer viverra erat. "
                          "Tellus elit ut in, nunc auctor dapibus sed enim.",
                  menuItem_id=11, user_id=3)
session.add(review15)
session.commit()

# Create a dummy review16
review16 = Review(rate=3,
                  content="Lorem ante vitae maecenas arcu, "
                          "ornare nonummy vitae amet sapien. "
                          "Eu quam dui aliquam, "
                          "ac vitae sit lacus tincidunt.",
                  menuItem_id=11, user_id=4)
session.add(review16)
session.commit()

# Create a dummy review17
review17 = Review(rate=5,
                  content="Lorem ipsum dolor sit amet, "
                          "consectetuer adipiscing elit. "
                          "Aenean commodo ligula eget dolor.",
                  menuItem_id=11, user_id=1)
session.add(review17)
session.commit()

# Create a dummy review18
review18 = Review(rate=5,
                  content="Metus condimentum sodales suspendisse "
                          "justo, quis dolor id wisi pellentesque, "
                          "nostra nunc fusce mi.",
                  menuItem_id=7, user_id=2)
session.add(review18)
session.commit()


# Create a dummy review19
review19 = Review(rate=3,
                  content="Porta vitae orci aliquam, "
                          "faucibus massa consectetuer viverra erat. "
                          "Tellus elit ut in, nunc auctor dapibus sed enim.",
                  menuItem_id=7, user_id=3)
session.add(review19)
session.commit()

# Create a dummy review20
review20 = Review(rate=3,
                  content="Lorem ante vitae maecenas arcu, "
                          "ornare nonummy vitae amet sapien. "
                          "Eu quam dui aliquam, "
                          "ac vitae sit lacus tincidunt.",
                  menuItem_id=9, user_id=4)
session.add(review20)
session.commit()

# Create a dummy review21
review21 = Review(rate=3,
                  content="Lorem ipsum dolor sit amet, "
                          "consectetuer adipiscing elit. "
                          "Aenean commodo ligula eget dolor.",
                  menuItem_id=9, user_id=1)
session.add(review21)
session.commit()

# Create a dummy review22
review22 = Review(rate=5,
                  content="Metus condimentum sodales suspendisse "
                          "justo, quis dolor id wisi pellentesque, "
                          "nostra nunc fusce mi.",
                  menuItem_id=9, user_id=2)
session.add(review22)
session.commit()


# Create a dummy review23
review23 = Review(rate=5,
                  content="Porta vitae orci aliquam, "
                          "faucibus massa consectetuer viverra erat. "
                          "Tellus elit ut in, nunc auctor dapibus sed enim.",
                  menuItem_id=13, user_id=3)
session.add(review23)
session.commit()

# Create a dummy review24
review24 = Review(rate=3,
                  content="Lorem ante vitae maecenas arcu, "
                          "ornare nonummy vitae amet sapien. "
                          "Eu quam dui aliquam, "
                          "ac vitae sit lacus tincidunt.",
                  menuItem_id=13, user_id=4)
session.add(review24)
session.commit()

# Create a dummy review25
review25 = Review(rate=5,
                  content="Lorem ipsum dolor sit amet, "
                          "consectetuer adipiscing elit. "
                          "Aenean commodo ligula eget dolor.",
                  menuItem_id=14, user_id=1)
session.add(review25)
session.commit()

# Create a dummy review26
review26 = Review(rate=5,
                  content="Metus condimentum sodales suspendisse "
                          "justo, quis dolor id wisi pellentesque, "
                          "nostra nunc fusce mi.",
                  menuItem_id=15, user_id=2)
session.add(review26)
session.commit()


# Create a dummy review27
review27 = Review(rate=1,
                  content="Porta vitae orci aliquam, "
                          "faucibus massa consectetuer viverra erat. "
                          "Tellus elit ut in, nunc auctor dapibus sed enim.",
                  menuItem_id=15, user_id=3)
session.add(review27)
session.commit()

# Create a dummy review28
review28 = Review(rate=2,
                  content="Lorem ante vitae maecenas arcu, "
                          "ornare nonummy vitae amet sapien. "
                          "Eu quam dui aliquam, "
                          "ac vitae sit lacus tincidunt.",
                  menuItem_id=14, user_id=4)
session.add(review28)
session.commit()

print "added menu items!"
