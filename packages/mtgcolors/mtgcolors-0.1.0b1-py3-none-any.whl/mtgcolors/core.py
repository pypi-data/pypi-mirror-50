# -*- coding: utf-8 -*-
from . import helpers

# source:
# https://mtg.gamepedia.com/Color
# https://magic.wizards.com/en/articles/archive/card-preview/designing-commander-2016-edition-2016-10-24
# https://boardgames.stackexchange.com/questions/11550/what-are-the-names-for-magics-different-colour-combinations

_colorNames = {
    "w": "White",
    "u": "Blue",
    "b": "Black",
    "r": "Red",
    "g": "Green",
    "uw": "Azorius (WU, White + Blue)",
    "rw": "Boros (WR, White + Red)",
    "bu": "Dimir (UB, Blue + Black)",
    "bg": "Golgari (BG, Black + Green)",
    "gr": "Gruul (RG, Red + Green)",
    "ru": "Izzet (UR, Blue + Red)",
    "bw": "Orzhov (WB, White + Black)",
    "br": "Rakdos (BR, Black + Red)",
    "gw": "Selesnya (WG, White + Green)",
    "gu": "Simic (UG, Green + Blue)",
    "bgw": "Abzan (WBG, White + Black + Green)",
    "ruw": "Jeskai (WUR, White + Blue + Red)",
    "bgu": "Sultai (UBG, Blue + Black + Green)",
    "brw": "Mardu (WBR, White + Black + Red)",
    "gru": "Temur (URG, Blue + Red + Green)",
    "guw": "Bant (WUG, White + Blue + Green)",
    "buw": "Esper (WUB, White + Blue + Black)",
    "bru": "Grixis (UBR, Blue + Black + Red)",
    "bgr": "Jund (BRG, Black + Red + Green)",
    "grw": "Naya (WRG, White + Red + Green)",
    "bruw": "Artifice (WUBR, White + Blue + Black + Red)",
    "bgru": "Chaos (UBRG, Blue + Black + Red + Green)",
    "bgrw": "Aggression (BRGW, Black + Red + Green + White)",
    "gruw": "Altruism (RGWU, Red + Green + White + Blue)",
    "bguw": "Growth (GWUB, Green + White + Blue + Black)",
    "wubrg": "Rainbow (WUBRG, White + Blue + Black + Red + Green)",
}


def __explain_color(colorKey):
    colorExplanations = {
        "w": "White puts value in the group, the community, and its civilization as a whole. White believes that suffering is a by-product of individuals not prioritizing the good of the group. White's ultimate goal is peace—a world where there is no unnecessary suffering, a world where life is as good as it can be for each individual, a world where everyone gets along and no one seeks to disturb the bonds of unity that White had worked so long to forge. To govern and protect its community, White makes use of and puts value in a number of broad concepts; morality (ethics, grace, truth), order (law, discipline, duty), uniformity (conformity, religion), and structure (government, planning, reason). White is a color commonly associated with good and justice, but if left unchecked or if everyone is not working toward the same unified goal, White can become authoritarian, inflexible, and capable of sacrificing a small group for the sake of a larger one. Everything necessary to preserve the laws, rules, and governance that White created. [read more](https://mtg.gamepedia.com/Color#White)",
        "u": "Blue is the color that wants perfection and looks on the world and sees opportunity to achieve that, figuring out what you could achieve with the right education, experience, and tools. For Blue, life is one of constant discovery as you keep seeking to better yourself. This way of living requires the right attitude. You have to be open to possibilities, but also not too hasty in action. Blue is methodical and exact and recognizes that there are many forces, even some that come from within, that lead an individual astray. It is better to think one's options out carefully and select correctly than to rush to a decision. Implicitly, in that general world view, blue believes in tabula rasa: every one of us is born a blank slate with the potential to become anything. One need only understand how, to make the change. So with this ill-formed goal before it, Blue reasons that if it is to make itself better, it must become capable of everything it could be capable of, for that is to \"merely add\" to its own capabilities. Blue believes it can't possibly be bad to acquire the potential for any conscious action. Thus, Blue, believing it is capable of changing anything if it understands the change, and believing it is imperative that it acquire every capability it could have, concludes that it is imperative that it understand change. As such, blue is the color most interested in technology and wants the latest and greatest version of whatever it is using. Moreover, blue decides that it must understand everything; for truly, understanding can only improve one's effectiveness in any task. To gain understanding, blue must acquire knowledge. Since knowledge itself will inform every other decision, blue forms its principle goal: omniscience, the knowledge of all. [read more](https://mtg.gamepedia.com/Color#Blue)",
        "b": "Black doesn't see anything as fundamentally immoral. To black, the only measure of right and wrong should be whether or not it leads to success. Black is open to opportunities and strategies rejected by others as taboo or forbidden—death, torment, infection, betrayal. Black characters will do anything to ensure their own well-being even at the expense of others; to black, anything less only allows others to do the same. Thus, black does everything possible to gain the only commodity that can secure it from weakness, and ensure its ability to get whatever it needs or wants—power. Although if taken to extremes, black's selfishness and lack of ethical restraint can result in tragedy, at its most basic level black is not inherently evil. It has a very cynical world view, and its core philosophy is that of self-determination and release from society-imposed limitations. Black has an ally in blue, as it appreciates its subtlety and use of cold logic. Black is also allied with red, respecting its desire to do things on its own terms. However, black's disregard for other members of the group, spirituality/religion, and the sanctity of life opposes it with green and white. [read more](https://mtg.gamepedia.com/Color#Black)",
        "r": "Above all else, Red values freedom. It wants to do what it wants, when it wants, to whom it wants, and nobody can tell it otherwise. In summary, Red thinks that all you have to do is listen to your heart and simply act accordingly, letting your emotions guide you. Red loves life much more than any other color and so it believes that all people must live to its fullest. Red believes that life is an adventure, that it would be much more fun if everyone stopped caring about rules, laws, and personal appearances and just spent their time indulging their desires through experience. Red doesn't live its life questioning choices it has made, and lives in the moment; Red is spontaneous and embraces every adventure put before it. Red is the color of immediate action and immediate gratification. If it wants something, it will act on its impulses and take it, regardless of the consequences. Red embraces relationships and knows passion and loyalty and camaraderie and lust. When Red bonds with another, it bonds strongly and fiercely. To outsiders, Red might seem a bit chaotic; that's only because others can't see what's in red's heart. Red sees order of any kind as pointlessly inhibiting, believing that only through embracing anarchy could everyone really be free to enjoy life to the fullest with no regrets. [read more](https://mtg.gamepedia.com/Color#Red)",
        "g": "Green doesn't want to change the world, it wants everybody to accept the world as it is. Green is convinced that the world already got everything right. Green tries to coexist with it instead of trying to change it, regulate it, norm it, or take advantage of it. Green is the color of nature and interdependence. It believes that the natural order is a thing of beauty and has all the answers to life's problems, that obeying the natural order alone is the best way to exist and thus favors a simplistic way of living in harmony with the rest of the world. This can often lead to it being perceived as a pacifistic color, as it does not seek to make conflict with the other colors as long as they leave it alone and do not disrespect nature. However, it is fierce when it feels threatened and can be predatory and aggressive if its instincts dictate. Green believes each individual is born with all the potential they need, that it's imprinted in its genes. That everyone was born with a role and that the goal is to recognize it and then embrace it, and thus do what they were destined to do. But that role interconnects with the web of life, and thus everyone has to learn how you fit into the larger picture. We are not alone, we are a part of a complex system full of interdependency. Green truly believes that every individual has to bother to sit back and understand the bigger picture and don't get so caught up in the details of their lives. [read more](https://mtg.gamepedia.com/Color#Green)",
        "uw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/slow-and-steady-2006-05-01-0)",
        "rw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/disorderly-conduct-2005-12-05-0)",
        "bu": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/pretty-sneaky-sis-2005-11-07-0)",
        "bg": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/life-and-death-2005-10-24-0)",
        "gr": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/aaaargh-2006-01-30-0)",
        "ru": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/creative-differences-2006-02-27-0)",
        "bw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/playing-their-own-rules-2006-03-27-0)",
        "br": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/hedonism-attitude-2006-08-14-0)",
        "gw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/group-think-2005-10-03-0)",
        "gu": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/improving-upon-nature-2006-05-22)",
        "bgw": "[read more](https://magic.wizards.com/en/articles/archive/mm/we-will-survive-2014-09-29)",
        "ruw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/smart-thinking-2014-11-03)",
        "bgu": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/whatever-it-takes-2015-02-02)",
        "brw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/finishing-first-2014-11-17)",
        "gru": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/what-doesnt-kill-you-makes-you-stronger-2015-02-23)",
        "guw": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/peace-love-and-understanding-2008-10-06)",
        "buw": "[read more](https://magic.wizards.com/en/articles/archive/feature/striving-perfection-2008-11-17)",
        "bru": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/looking-out-number-one-2008-10-17)",
        "bgr": "[read more](https://magic.wizards.com/en/articles/archive/making-magic/following-your-heart-2008-12-01)",
        "grw": "[read more](https://magic.wizards.com/en/articles/archive/feature/searching-within-2008-11-03)",
        "bruw": "White embraces the progress exemplified in civilization. Blue finds technology fascinating. Black sees no moral distinction between the natural and the artificial. Red is happy to create and to destroy. But green? Green hates all of these things!",
        "bgru": "Blue is eager to discover the results of empirical experiments. Black is happy to confuse its enemies. Red embraces chaos on an elemental level as an essential part of its nature. Green is content to let the universe unfold as it will. White, as the color of order and structure, tries to contain chaos at every turn—but chaos will not be contained!",
        "bgrw": "Black believes in strangling the young before they grow up to become a threat. Red loves to fight for the sheer exhilaration of it. Green understands that survival of the fittest makes the whole of nature strong, and white is willing to fight to defend its people and its beliefs. Blue, however, would prefer to slow down and study the situation in order to find the correct solution.",
        "gruw": "Red loves its friends. Green understands the power of symbiosis. White believes in community above all else. Blue values knowledge, and believes that it should be shared freely. Black sees selfishness as a virtue and believes that altruism only encourages weakness.",
        "bguw": "Green appreciates that a mighty oak grows from a tiny seed. White is the great builder of civilizations. Blue wants to expand its understanding. Black wants to increase its power. Red, acting on impulse, cares not about the future and only wants what it can have now, now, now!",
        "wubrg": "WUBRG is often called rainbow because a rainbow contains all colors. Beside, it is easier to pronounce. By the way, WUBRG's phonetic transcription is /wu'bɜːɹg/.",
    }

    if colorKey in colorExplanations and colorExplanations[colorKey]:
        return colorExplanations[colorKey]

    return "no additional informations available"


def __find_colors_with_wildcard(loweredInput):
    key = "".join(sorted(loweredInput.replace("x", "")))
    keys = list(_colorNames.keys())
    length = len(loweredInput)
    inputs = list(
        filter(lambda k: len(k) == length and helpers.isContained(key, k), keys)
    )
    choices = list(map(lambda x: __build_color(x, False), inputs))
    return (
        "Available choices are:\n* " + "\n* ".join(sorted(choices)) if choices else ""
    )


def __find_color(input):
    return _colorNames[input] if input in _colorNames else input


def __find_key(key):
    colorKeys = {
        "w": "w",
        "white": "w",
        "u": "u",
        "blue": "u",
        "b": "b",
        "black": "b",
        "r": "r",
        "red": "r",
        "g": "g",
        "green": "g",
        "uw": "uw",
        "azorius": "uw",
        "rw": "rw",
        "boros": "rw",
        "bu": "bu",
        "dimir": "bu",
        "bg": "bg",
        "golgari": "bg",
        "gr": "gr",
        "gruul": "gr",
        "ru": "ru",
        "izzet": "ru",
        "bw": "bw",
        "orzhov": "bw",
        "br": "br",
        "rakdos": "br",
        "mono-rakdos": "br",
        "gw": "gw",
        "selesnya": "gw",
        "gu": "gu",
        "simic": "gu",
        "bgw": "bgw",
        "abzan": "bgw",
        "necra": "bgw",
        "teneb": "bgw",
        "junk": "bgw",
        "doran": "bgw",
        "ruw": "ruw",
        "jeskai": "ruw",
        "numot": "ruw",
        "raka": "ruw",
        "bgu": "bgu",
        "sultai": "bgu",
        "ana": "bgu",
        "vorosh": "bgu",
        "brw": "brw",
        "mardu": "brw",
        "oros": "brw",
        "dega": "brw",
        "gru": "gru",
        "temur": "gru",
        "ceta": "gru",
        "intet": "gru",
        "guw": "guw",
        "bant": "guw",
        "buw": "buw",
        "esper": "buw",
        "bru": "bru",
        "grixis": "bru",
        "bgr": "bgr",
        "jund": "bgr",
        "grw": "grw",
        "naya": "grw",
        "bruw": "bruw",
        "artifice": "bruw",
        "yore": "bruw",
        "yore-tiller": "bruw",
        "non-green": "bruw",
        "bgru": "bgru",
        "chaos": "bgru",
        "glint": "bgru",
        "glint-eye": "bgru",
        "non-white": "bgru",
        "bgrw": "bgrw",
        "aggression": "bgrw",
        "dune": "bgrw",
        "dune-brood": "bgrw",
        "non-blue": "bgrw",
        "gruw": "gruw",
        "altruism": "gruw",
        "ink": "gruw",
        "ink-treader": "gruw",
        "non-black": "gruw",
        "bguw": "bguw",
        "growth": "bguw",
        "witch": "bguw",
        "witch-maw": "bguw",
        "non-red": "bguw",
        "rainbow": "wubrg",
        "wubrg": "wubrg",
        "domain": "wubrg",
        "five-color": "wubrg",
    }

    return colorKeys[key] if key in colorKeys else ""


def __build_output(key, isVerbose):
    return __find_color(key) + ("\n" + __explain_color(key) if isVerbose else "")


def __build_color(loweredInput, isVerbose):
    key = __find_key(loweredInput)
    if key:
        return __build_output(key, isVerbose)

    orderedInput = "".join(sorted(loweredInput))
    key = __find_key(orderedInput)
    if key:
        return __build_output(key, isVerbose)

    if not "x" in loweredInput:
        return "key not found"

    result = __find_colors_with_wildcard(loweredInput)
    return result if result else "key not found"


def clarify(source, isVerbose=False):
    if not source or source.isspace():
        raise ValueError("empty string")

    return __build_color(source.lower(), isVerbose)


# if __name__ == "__main__":
#     unittest.main()
# print(clarify(" ".join(sys.argv)))
