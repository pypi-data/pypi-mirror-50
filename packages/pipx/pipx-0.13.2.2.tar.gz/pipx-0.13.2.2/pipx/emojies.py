from pipx.util import emoji_support

if emoji_support:
    stars = "✨ 🌟 ✨"
    hazard = "⚠️"
    sleep = "😴"
else:
    stars = ""
    hazard = ""
    sleep = ""
