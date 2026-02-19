import random
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


def wrap(text: str, width: int = 88) -> str:
    return "\n".join(textwrap.fill(line, width=width) for line in text.splitlines())


@dataclass
class StoryNode:
    node_id: str
    text: str
    choices: Dict[str, Tuple[str, str]] = field(default_factory=dict)
    is_ending: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class StoryState:
    genre: str
    tone: str
    protagonist: str
    companion: str
    world_seed: int
    inventory: List[str] = field(default_factory=list)
    flags: Dict[str, int] = field(default_factory=dict)

    def summary(self) -> str:
        collected = ", ".join(self.inventory) if self.inventory else "nothing"
        return (
            f"Genre: {self.genre}, tone: {self.tone}. Protagonist: {self.protagonist} "
            f"with {self.companion}. Inventory: {collected}. Flags: {self.flags}"
        )


class StoryGenerator:
    def __init__(self, state: StoryState):
        self.state = state
        self.rand = random.Random(state.world_seed)

    def generate_opening(self) -> StoryNode:
        world = self._world_description()
        hook = self._inciting_incident()
        text = (
            f"In a {self.state.tone} {self.state.genre} world, {self.state.protagonist} "
            f"travels with {self.state.companion}. {world} {hook}\n\n"
            "What will you do?"
        )
        choices = {
            "A": ("Investigate the omen", "omen"),
            "B": ("Seek an ally in the nearest settlement", "ally"),
            "C": ("Ignore it and press onward", "onward"),
        }
        return StoryNode("opening", text, choices)

    def generate_omen(self) -> StoryNode:
        clue = self._mysterious_clue()
        text = (
            f"The air shivers as runes flicker across the path. {self.state.companion} "
            f"whispers about old tales. You notice {clue}.\n\nWill you:"
        )
        choices = {
            "A": ("Study the runes closely", "study_runes"),
            "B": ("Mark the site and retreat for now", "retreat"),
            "C": ("Touch the brightest rune", "touch_rune"),
        }
        return StoryNode("omen", text, choices)

    def generate_study_runes(self) -> StoryNode:
        text = (
            f"As {self.state.protagonist} studies the runes, {self.state.companion} gasps — "
            "the symbols start rearranging themselves into a path only visible under moonlight. "
            "The markings pulse gently, revealing a hidden direction.\n\n"
            "What will you do next?"
        )
        choices = {
            "A": ("Follow the glowing path", "hidden_path"),
            "B": ("Copy the runes for later study", "onward"),
            "C": ("Erase one and see what happens", "climax"),
        }
        return StoryNode("study_runes", text, choices)

    def generate_ally(self) -> StoryNode:
        ally_name = self._ally_name()
        text = (
            f"At the settlement, a wary figure named {ally_name} offers guidance for a price. "
            f"They speak of a hidden way only the persistent may find.\n\nChoose:"
        )
        choices = {
            "A": ("Barter a keepsake for their map", "get_map"),
            "B": ("Earn trust by helping with a local problem", "help_local"),
            "C": ("Refuse and chart your own route", "onward"),
        }
        return StoryNode("ally", text, choices)

    def generate_onward(self) -> StoryNode:
        terrain = self._terrain()
        text = (
            f"You press onward into {terrain}. The path splits before a stone arch. "
            f"Beneath the moss, faint grooves suggest something is missing.\n\nDo you:" 
        )
        choices = {
            "A": ("Search the area for a fitting object", "search_area"),
            "B": ("Force your way through the arch", "force_arch"),
            "C": ("Set camp and wait for signs", "make_camp"),
        }
        return StoryNode("onward", text, choices)

    def generate_hidden_path(self) -> StoryNode:
        text = (
            "You feel a shift in the world: a narrow passage reveals itself where shadows "
            "overlap. Few ever notice this place. A hush falls as if the story itself is "
            "holding its breath.\n\nProceed?"
        )
        choices = {
            "A": ("Enter the hidden passage", "hidden_depths"),
            "B": ("Mark it and return later", "return_later"),
            "C": ("Call out into the dark", "call_dark"),
        }
        return StoryNode("hidden_path", text, choices, tags=["hidden"])

    def generate_climax(self) -> StoryNode:
        force = self._antagonistic_force()
        text = (
            f"At last, you confront {force}. Threads of fate tighten around {self.state.protagonist}.\n"
            "The outcome turns on a single choice.\n\nChoose your stand:"
        )
        choices = {
            "A": ("Appeal with empathy", "ending_hopeful"),
            "B": ("Outwit with a bold gambit", "ending_twist"),
            "C": ("Defy at any cost", "ending_tragic"),
        }
        return StoryNode("climax", text, choices)

    def generate_ending(self, style: str) -> StoryNode:
        base = (
            f"After all trials, {self.state.protagonist} and {self.state.companion} "
            f"face the consequences. {self._ending_fragment(style)}\n\n"
            f"This chapter closes in a {style} way."
        )
        return StoryNode(f"ending_{style}", base, {}, is_ending=True, tags=["ending", style])

    # --- Internal content helpers ---
    def _world_description(self) -> str:
        motifs = {
            "fantasy": [
                "ancient forests hum with latent magic",
                "ruins dream beneath ivy and star-shards",
                "dragons are rumors woven into lullabies",
            ],
            "sci-fi": [
                "neon skylines flicker over rusted megastructures",
                "fractured moons glow above orbital shipyards",
                "synthetic dawns reboot forgotten cities",
            ],
            "mystery": [
                "fog erases footprints faster than they form",
                "clocks tick out-of-sync with the heart",
                "every window watches with a different story",
            ],
        }
        key = self._closest_key(self.state.genre, motifs)
        return self.rand.choice(motifs[key]).capitalize() + "."

    def _inciting_incident(self) -> str:
        incidents = [
            "A comet carves a silent arc and leaves a whispering tail.",
            "A letter arrives signed by a future version of you.",
            "The river flows backward for exactly one minute.",
            "A bell rings where there is no bell.",
        ]
        return self.rand.choice(incidents)

    def _mysterious_clue(self) -> str:
        clues = [
            "a rune repeating the shape of your heartbeat",
            "ash arranged like a compass pointing underground",
            "a soft tone audible only when eyes are closed",
            "footprints that avoid every puddle",
        ]
        return self.rand.choice(clues)

    def _ally_name(self) -> str:
        first = ["Iria", "Thorne", "Vel", "Mara", "Kade", "Nyx", "Quen"]
        last = ["Ashfall", "Kestrel", "Voss", "Hallow", "Strand", "Noct"]
        return f"{self.rand.choice(first)} {self.rand.choice(last)}"

    def _terrain(self) -> str:
        terrains = [
            "wind-scoured valley",
            "tangle of luminous reeds",
            "labyrinth of basalt spires",
            "glimmering salt flats",
        ]
        return self.rand.choice(terrains)

    def _antagonistic_force(self) -> str:
        forces = [
            "the Archivist who edits memories",
            "the Clock that refuses to strike midnight",
            "the Leviathan beneath the city",
            "the Choir of Masks that speaks as one",
        ]
        return self.rand.choice(forces)

    def _ending_fragment(self, style: str) -> str:
        if style == "hopeful":
            return (
                "Kindness accumulates like dawn. Promises once broken are rewoven, and the "
                "road ahead gleams with possibility."
            )
        if style == "tragic":
            return (
                "A necessary loss settles like snow. What is saved endures because of what "
                "was given up."
            )
        return (
            "Nothing was as it seemed: the question mattered more than the answer, and "
            "the answer changes when observed."
        )

    def _closest_key(self, key: str, mapping: Dict[str, List[str]]) -> str:
        k = key.strip().lower()
        if k in mapping:
            return k
        for candidate in mapping.keys():
            if candidate.startswith(k[:3]):
                return candidate
        return next(iter(mapping.keys()))


class StoryEngine:
    SECRET_INPUT = "whisper"

    def __init__(self, state: StoryState):
        self.state = state
        self.gen = StoryGenerator(state)
        self.nodes = self._build_nodes()
        self.current_id = "opening"

    def _build_nodes(self) -> Dict[str, StoryNode]:
        nodes = {
            "opening": self.gen.generate_opening(),
            "omen": self.gen.generate_omen(),
            "study_runes": self.gen.generate_study_runes(),  # ✅ FIX ADDED
            "ally": self.gen.generate_ally(),
            "onward": self.gen.generate_onward(),
            "hidden_path": self.gen.generate_hidden_path(),
            "climax": self.gen.generate_climax(),
            "ending_hopeful": self.gen.generate_ending("hopeful"),
            "ending_tragic": self.gen.generate_ending("tragic"),
            "ending_twist": self.gen.generate_ending("twist"),
        }
        return nodes

    def restart_with(self, new_state: StoryState) -> None:
        self.state = new_state
        self.gen = StoryGenerator(new_state)
        self.nodes = self._build_nodes()
        self.current_id = "opening"

    def step(self, user_input: str) -> Optional[StoryNode]:
        user_input = user_input.strip()
        node = self.nodes[self.current_id]

        if user_input.startswith(":"):
            self._handle_command(user_input[1:])
            return self.nodes[self.current_id]

        if user_input.lower() == self.SECRET_INPUT:
            self.state.flags["secret"] = self.state.flags.get("secret", 0) + 1
            self.current_id = "hidden_path"
            return self.nodes[self.current_id]

        if node.node_id == "omen" and user_input.upper() == "A":
            self.state.flags["studies"] = self.state.flags.get("studies", 0) + 1
            if self.state.flags["studies"] >= 2:
                self.current_id = "hidden_path"
                return self.nodes[self.current_id]

        if user_input.upper() in node.choices:
            _, next_id = node.choices[user_input.upper()]
            self._apply_side_effects(node.node_id, user_input.upper())
            self.current_id = next_id
            return self._maybe_funnel_to_climax()

        return None

    def _maybe_funnel_to_climax(self) -> StoryNode:
        self.state.flags["steps"] = self.state.flags.get("steps", 0) + 1
        node = self.nodes.get(self.current_id)
        if node is None:
            # safety fallback
            self.current_id = "climax"
            return self.nodes["climax"]
        if (
            not node.is_ending
            and "hidden" not in node.tags
            and self.state.flags.get("steps", 0) >= 4
            and any(k for k in self.state.flags.keys() if k not in ("steps",))
        ):
            self.current_id = "climax"
            return self.nodes["climax"]
        return node

    def _apply_side_effects(self, node_id: str, choice: str) -> None:
        if node_id == "ally" and choice == "A":
            self.state.inventory.append("cryptic map")
            self.state.flags["map"] = 1
        if node_id == "onward" and choice == "A":
            self.state.inventory.append("stone key")
            self.state.flags["key"] = 1
        if node_id == "omen" and choice == "C":
            self.state.flags["reckless"] = 1
        if node_id == "onward" and choice == "B":
            self.state.flags["wounded"] = 1

    def get_current_node(self) -> StoryNode:
        return self.nodes[self.current_id]

    def rewrite_ending(self, style: str) -> None:
        style_key = style.strip().lower()
        if style_key not in ("hopeful", "tragic", "twist"):
            style_key = "twist"
        self.nodes[f"ending_{style_key}"] = self.gen.generate_ending(style_key)
        self.current_id = f"ending_{style_key}"

    def _handle_command(self, cmd: str) -> None:
        parts = cmd.split()
        if not parts:
            return
        head, *tail = parts
        if head == "help":
            print(wrap(
                "Commands: :help, :state, :inv, :rewrite [hopeful|tragic|twist], "
                ":restart, :seeds, :quit"
            ))
        elif head == "state":
            print(wrap(self.state.summary()))
        elif head == "inv":
            print(wrap(", ".join(self.state.inventory) if self.state.inventory else "(empty)"))
        elif head == "rewrite":
            style = tail[0] if tail else "twist"
            self.rewrite_ending(style)
        elif head == "restart":
            new = prompt_for_seeds()
            self.restart_with(new)
        elif head == "seeds":
            print(wrap(
                "You can type :restart to regenerate the whole story with new seeds. "
                f"Current seed: {self.state.world_seed}"
            ))
        elif head == "quit":
            raise SystemExit(0)


def prompt_for_seeds() -> StoryState:
    print(wrap("Let's set up your story world. Leave blank for defaults."))
    genre = input("Genre (fantasy/sci-fi/mystery): ").strip() or "fantasy"
    tone = input("Tone (whimsical/grim/serene): ").strip() or "whimsical"
    protagonist = input("Protagonist name: ").strip() or "Ari"
    companion = input("Companion name: ").strip() or "Rook"
    seed_str = f"{genre}|{tone}|{protagonist}|{companion}"
    world_seed = abs(hash(seed_str)) % (2**31 - 1)
    return StoryState(
        genre=genre,
        tone=tone,
        protagonist=protagonist,
        companion=companion,
        world_seed=world_seed,
    )


def print_node(node: StoryNode) -> None:
    print()
    print(wrap(node.text))
    if node.choices:
        print()
        for key, (label, _) in node.choices.items():
            print(f"  {key}. {label}")
    print()
    print(wrap("(Type A/B/C to choose, or commands like :help, :state, :inv, :rewrite)"))
    print(wrap(f"Hint: type '{StoryEngine.SECRET_INPUT}' at any time to seek hidden paths."))


def main() -> None:
    print(wrap(
        "AI-Like Interactive Storybook\n" 
        "You shape the tale by choosing paths, discovering secrets, and rewriting endings."
    ))
    state = prompt_for_seeds()
    engine = StoryEngine(state)

    while True:
        node = engine.get_current_node()
        print_node(node)
        if node.is_ending:
            choice = input(
                "You reached an ending. Type :rewrite [style], :restart, or press Enter to continue: "
            ).strip()
            if choice:
                try:
                    engine.step(":" + choice if not choice.startswith(":") else choice)
                except SystemExit:
                    break
            else:
                styles = ["hopeful", "twist", "tragic"]
                style = styles[random.randint(0, 2)]
                engine.rewrite_ending(style)
            continue

        user = input("Your choice (A/B/C, :command, or 'whisper' for hidden): ")
        try:
            next_node = engine.step(user)
        except SystemExit:
            break

        if next_node is None:
            print(wrap("I didn't understand that. Try A/B/C, a command (like :help), or 'whisper'."))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye.")