from app.internal import chunking, agent_data, response_agent
from sklearn.metrics.pairwise import cosine_similarity as cs
from openai import Embedding
import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
import app.internal.tokenizer as tokenizer
import uuid
import numpy as np
import time
import random




string = """Once upon a time in a far-off kingdom, nestled among rolling hills and dense forests, there lived a young girl named Elara. She had the kind of curiosity that couldn't be satiated by the stories and chores of her small village. Elara's heart yearned for adventure, for the kind of tales she read in the old books she found in her grandmother's attic. These books spoke of ancient magic, hidden worlds, and creatures of light and shadow.

Elara's life took a turn one crisp autumn evening when a mysterious comet streaked across the sky, its tail glittering with a thousand colors. That night, as she lay in bed, a soft glow seeped through her window, and a gentle voice called to her. It was an ethereal creature, a guardian of the ancient forest, who had come seeking Elara's help. The Heart of the Forest, a magical gem that balanced nature and protected the kingdom, had been stolen. Without it, the kingdom would fall into darkness and despair.

The guardian explained that the comet was a sign, a beacon for the one who could retrieve the Heart. Elara, with her pure heart and brave soul, was the chosen one. Despite her fears and the enormity of the task ahead, Elara felt a fire ignite within her. She knew this was the adventure she had always dreamt of.

With a small pack of provisions and a compass given to her by the guardian, Elara set out at dawn. Her journey led her through enchanted forests where the trees whispered secrets, over mountains where the wind told tales of ancient times, and across rivers that sparkled with the magic of the Heart. Along the way, Elara met allies who would become dear friends: a wise fox who could speak to the wind, a knight who had lost his way but not his courage, and a sorceress with knowledge of the old magics.

The group faced many challenges, from trickster spirits and labyrinthine caves to a sea of endless dreams that tested their resolve. Each trial taught Elara something new about herself and the power of friendship and determination.

Their quest led them to the Dark Castle, a place shrouded in shadows and ruled by a sorcerer who had stolen the Heart of the Forest. It was here that Elara's courage was tested like never before. The sorcerer was powerful, but Elara and her friends fought with the strength of their bond and the righteousness of their cause. In the castle's deepest chamber, amidst a battle of magic and wits, Elara reclaimed the Heart of the Forest.

With the Heart restored to its rightful place, balance was returned to the kingdom. The forests grew lush and green, the rivers flowed with sparkling waters, and the people rejoiced in the return of peace and prosperity. Elara, once a simple village girl, had become a hero. But more importantly, she had discovered her true self—a brave, kind, and adventurous soul who had changed the fate of her world.

As she returned to her village, greeted by cheers and admiration, Elara knew that this was only the beginning of her adventures. For the world was vast, and countless stories awaited her. And so, with her friends by her side, Elara looked to the horizon, ready for whatever came next, her heart beating with the promise of new tales to tell.

And they all lived happily ever after, but not in the way of old tales, for their happiness was in their continued adventures, the friendships they cherished, and the knowledge that together, they could face any challenge the world threw their way.

The end."""


str_2 = """In a remote corner of the world, where the sea kisses the sky on the horizon, there stood an ancient lighthouse. It had weathered many storms and had been a beacon of hope for countless sailors navigating the treacherous waters. The lighthouse keeper, an old man named Elias, was as much a part of the lighthouse as it was of him. With a thick beard as white as the crest of the waves and eyes that mirrored the depth of the ocean, Elias had dedicated his life to maintaining the light that guided ships to safety.

Elias lived a solitary life, with only the sea birds and the rhythm of the waves for company. His days were marked by the routine of polishing the lighthouse's lens, refueling the lamp, and recording the weather. However, Elias harbored a secret that had been passed down through generations of lighthouse keepers before him. Beneath the lighthouse, accessible only through a hidden trapdoor in the floor of his modest living quarters, lay a cavern that stretched deep into the earth.

This cavern was home to an ancient library, filled with shelves carved into the very rock that held the weight of the lighthouse above. These shelves were laden with books and scrolls, some as ancient as the lighthouse itself. This secret library contained the knowledge of the sea, detailing every creature that dwelled within its depths, every storm that had ever raged across its surface, and maps of underwater realms that human eyes had never seen.

Elias spent his nights poring over these texts, learning the secrets of the sea. He discovered tales of lost civilizations submerged beneath the waves, of great sea monsters that lurked in the darkest depths, and of enchanted items that had the power to calm the fiercest storms. Elias believed that this knowledge was a sacred trust, a gift from the sea itself, meant to be safeguarded for the benefit of all humanity.

But the world outside the lighthouse was changing. Modern technology had begun to render lighthouses obsolete, and there were whispers that Elias's lighthouse would soon be decommissioned. Fearing that the ancient knowledge would be lost forever if the lighthouse were abandoned, Elias made a decision that would change the course of his life.

He began to venture into the nearby town, sharing stories of the sea with anyone who would listen. At first, people were skeptical of the old lighthouse keeper's tales, but soon, his stories captivated the hearts and minds of the townsfolk. Scientists and scholars came to hear of Elias's library, and he welcomed them into his secret world, teaching them the mysteries contained within the ancient texts.

As word of the lighthouse keeper's secret spread, the lighthouse became a beacon of knowledge, a place where people from all walks of life could come to learn about the wonders of the sea. The government, recognizing the value of the knowledge preserved by Elias, declared the lighthouse a heritage site, ensuring its preservation for generations to come.

Elias, once a solitary guardian of the light, had become the keeper of a far greater treasure. He had shown the world that knowledge, like the light of a lighthouse, is meant to be shared, illuminating the darkness and guiding humanity forward. And as the sun set on the horizon, casting its golden light across the sea, the lighthouse stood tall, a symbol of hope, guidance, and the enduring power of knowledge."""


str_3 = '''In a small town nestled at the foot of a great mountain, there lived a young girl named Clara. Clara was known throughout the town for her boundless curiosity and adventurous spirit. She had explored every nook and cranny of the town and the surrounding countryside, but what fascinated her most was the great mountain that towered over their home. It was said that at the summit of the mountain lay a secret garden, hidden from the eyes of the ordinary, a place of unparalleled beauty and magic.

Despite the warnings of the townsfolk, who spoke of treacherous paths and fierce creatures guarding the way, Clara's heart was set on discovering the secret garden. She spent days preparing, reading old maps, and listening to the tales of those who had ventured partway up the mountain. With a sturdy backpack filled with supplies, Clara set off at dawn, her eyes alight with the promise of adventure.

The path was steep and winding, taking Clara through dense forests where sunlight barely touched the ground. She crossed sparkling streams and climbed rugged outcrops, each step taking her higher and closer to the clouds. Along the way, Clara encountered creatures of the mountain: wise owls that shared their wisdom, nimble goats that showed her the safest paths, and even a grumpy old bear who, after some persuasion, shared his knowledge of the mountain's secrets.

Days turned into weeks, and Clara persevered, her determination never waning. She learned to listen to the mountain, to understand its whispers and warnings. And then, when she had almost given up hope, she found it. Hidden behind a waterfall, its mist casting rainbows in the sunlight, was the entrance to the secret garden.

Stepping through the waterfall, Clara entered a world unlike any she had ever seen. Flowers of every color and size bloomed in abundance, their fragrances blending into a perfume that filled the air with sweetness. Fruit trees laden with jewels of nature's bounty offered sustenance, and crystal-clear ponds teemed with fish that shimmered like stars in the night sky. In the center of the garden stood a magnificent tree, its branches reaching out as if embracing the sky, and beneath it, a spring of clear water that sparkled with the light of the sun.

Clara spent days in the garden, exploring its wonders and uncovering its secrets. She learned that the garden was alive, its magic sustained by the harmony of nature. It was a place of healing and peace, a gift to those who respected and protected the balance of the natural world.

When Clara finally returned to her town, she was not the same girl who had left in search of adventure. She carried with her the wisdom of the mountain and the magic of the secret garden. She spoke of the importance of living in harmony with nature, of protecting the beauty that lay not just at the summit of great mountains but all around them. Clara's journey became a legend, inspiring others to seek the magic in the world, to listen to the whispers of the earth, and to protect the beauty that exists everywhere, if only one has the courage to seek it.

And so, the secret garden remained, a testament to the magic that lies in the heart of nature, waiting for those brave enough to discover it.'''




agent = response_agent.Agent(instruction="assistant", json_mode = False, model="gpt-3.5-turbo-0125")
agent.inject_memory(string)
agent.inject_memory(str_2)
agent.inject_memory(str_3)
agent.chat("is elara happy")







time_init = time.time()
results = data.query("Elara and Clara, are they related?")
time_end = time.time()
print("Time to query: ", time_end - time_init)

len(results)
for result in results:
    print(result)
    print('\n\n\n')
    
string_recons=" ".join([result for result in results])
tokenizer.count_tokens(string_recons)


tokenizer.count_tokens(str_2)