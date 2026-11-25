from abc import ABC, abstractmethod


# --- Product ---
class Story:
    def __init__(self, platform):
        self.platform = platform
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def show(self):
        print(f"{self.platform} Story parts: {', '.join(self.parts)}")


# --- Abstract Builder ---
class Builder(ABC):
    @property
    @abstractmethod
    def story(self) -> Story:
        pass

    @abstractmethod
    def build_image(self):
        pass

    @abstractmethod
    def build_music(self):
        pass

    @abstractmethod
    def build_special_effects(self):
        pass

    @abstractmethod
    def build_video(self):
        pass


# --- Concrete Builders ---
class FacebookConcreteBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._story = Story("Facebook")

    @property
    def story(self) -> Story:
        story = self._story
        self.reset()
        return story

    def build_image(self):
        self._story.add("Facebook Image")

    def build_music(self):
        self._story.add("Facebook Music Track")

    def build_special_effects(self):
        self._story.add("Facebook AR Filter")

    def build_video(self):
        self._story.add("Facebook Video Clip")


class InstagramConcreteBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._story = Story("Instagram")

    @property
    def story(self) -> Story:
        story = self._story
        self.reset()
        return story

    def build_image(self):
        self._story.add("Instagram Photo")

    def build_music(self):
        self._story.add("Instagram Reels Audio")

    def build_special_effects(self):
        self._story.add("Instagram Sparkle Effect")

    def build_video(self):
        self._story.add("Instagram Reel Video")


# --- Director ---
class StoryDirector:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder):
        self._builder = builder

    def build_basic_story(self):
        self._builder.build_image()

    def build_photo_music_story(self):
        self._builder.build_image()
        self._builder.build_music()
        self._builder.build_special_effects()

    def build_video_story(self):
        self._builder.build_video()
        self._builder.build_music()


if __name__ == "__main__":
    director = StoryDirector()

    # 1. Build Facebook stories
    fb_builder = FacebookConcreteBuilder()
    director.builder = fb_builder

    print("--- Facebook Stories ---")
    director.build_basic_story()
    fb_builder.story.show()

    director.build_photo_music_story()
    fb_builder.story.show()

    # 2. Build Instagram stories
    ig_builder = InstagramConcreteBuilder()
    director.builder = ig_builder

    print("\n--- Instagram Stories ---")
    director.build_video_story()
    ig_builder.story.show()

    # 3. Custom story without Director
    print("\n--- Custom Instagram Story ---")
    ig_builder.build_image()
    ig_builder.build_special_effects()
    ig_builder.story.show()