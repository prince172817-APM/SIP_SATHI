import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SIP Saathi Discovery Engine",
    page_icon="🔎",
    layout="wide",
)

# ------------------------------------------------------------
# 1. EVIDENCE: public sources collected for this project.
#    Each "text" is a short paraphrase written for this project,
#    with the original source linked.
# ------------------------------------------------------------
EVIDENCE = [
    {
        "id": "E1",
        "source": "Groww Help Centre: why did my SIP instalment fail",
        "type": "Official help page",
        "url": "https://groww.in/help/mutual-funds/order/why-did-my-sip-installment-fail--36",
        "text": "An SIP instalment fails when the SIP is not linked to an approved AutoPay.",
    },
    {
        "id": "E2",
        "source": "Groww Help Centre: AutoPay approved but SIP failed",
        "type": "Official help page",
        "url": "https://groww.in/help/mutual-funds/searchable/my-autopay-is-approved-even-then-my-sip-failed",
        "text": "Biller approval takes about 7 working days and OTP AutoPay about 21, and an SIP can still fail for several reasons even after approval.",
    },
    {
        "id": "E3",
        "source": "Jupiter community: could not create AutoPay on Groww",
        "type": "User forum post",
        "url": "https://community.jupiter.money/t/not-able-to-create-autopay-on-groww/31187",
        "text": "A user tried several times to create a Groww AutoPay mandate and kept getting an invalid debit card error. The card belonged to a different bank than the one selected.",
    },
    {
        "id": "E4",
        "source": "r/IndiaInvestments (2021): mandate for AutoPay in Groww",
        "type": "User forum post",
        "url": "https://libreddit.winscloud.net/r/IndiaInvestments/comments/qmdq75/mandate_for_autopay_in_groww_specifies_groww_as",
        "text": "An investor asks why the AutoPay mandate names Groww as the beneficiary and whether entering an ATM PIN is safe. Another says money was debited on the 3rd although the SIP date was the 8th.",
    },
    {
        "id": "E5",
        "source": "Outlook Business: penalty on failed SIP auto-debit",
        "type": "News report",
        "url": "https://www.outlookbusiness.com/ampstories/markets/penalty-on-failed-sip-auto-debit-higher-than-investment-amount-why-is-it-harmful-for-small-investors",
        "text": "A Reddit user said a bank charged Rs 590 for one failed SIP auto-debit. An expert warned that heavy penalties can put small investors off long-term investing.",
    },
    {
        "id": "E6",
        "source": "Groww Help Centre: ECS charges",
        "type": "Official help page",
        "url": "https://groww.in/help/mutual-funds/mf-autopay/what-are-ecs-charges--96",
        "text": "Groww states it does not charge anything when an SIP order fails.",
    },
    {
        "id": "E7",
        "source": "Groww Help Centre: pay an instalment after AutoPay failed",
        "type": "Official help page",
        "url": "https://groww.in/help/mutual-funds/mf-sip/how-do-i-pay-for-my-sip-installment-if-the-autopay-debit-has-failed--40",
        "text": "Groww has a dedicated help article on paying an instalment manually after an AutoPay debit fails.",
    },
    {
        "id": "E8",
        "source": "Groww Help Centre: can I pause my SIP",
        "type": "Official help page",
        "url": "https://groww.in/help/mutual-funds/order/can-i-pause-sip-for-next-month",
        "text": "Groww lets investors pause an upcoming SIP instalment through Edit SIP.",
    },
    {
        "id": "E9",
        "source": "Angel One news: SIP stoppage ratio, September 2026 (AMFI data)",
        "type": "Industry data",
        "url": "https://www.angelone.in/news/mutual-funds/sip-stoppage-ratio-falls-for-5th-straight-month-to-78-53-in-september-2026",
        "text": "The SIP stoppage ratio was 78.53% in September 2026, down from 95.46% in May. It counts SIPs discontinued or completed against new registrations.",
    },
    {
        "id": "E10",
        "source": "Angel One news: SIP stoppage ratio, April 2026 (AMFI data)",
        "type": "Industry data",
        "url": "https://www.angelone.in/news/mutual-funds/new-sip-registrations-drop-to-12-month-low-in-april-2026-amid-rising-closures",
        "text": "The stoppage ratio reached 101% in April 2026, meaning more SIPs were closed than opened.",
    },
]

# ------------------------------------------------------------
# 2. THEMES: keyword scoring (rule-based, not generative AI).
#    Order matters: on a tie, the earlier theme wins.
# ------------------------------------------------------------
THEMES = {
    "Setup confusion and trust": {
        "keywords": ["confus", "invalid", "beneficiary", "atm pin", "safe",
                     "different bank", "error", "set up", "setup", "not sure"],
        "opportunity": "Explain AutoPay in plain language with a safe-setup checklist (SIP Saathi topic: AutoPay mandate problem).",
    },
    "Cost and penalty worry": {
        "keywords": ["charge", "penalt", "fee", "rs ", "ecs", "cost"],
        "opportunity": "State clearly who may charge (platform or bank) and how to avoid bounce charges.",
    },
    "Payment failure and AutoPay approval": {
        "keywords": ["fail", "autopay", "mandate", "approv", "debit",
                     "bounce", "insufficient"],
        "opportunity": "Failed Payment Guidance: likely cause plus the next step (SIP Saathi topics: Failed SIP payment, Missed SIP instalment).",
    },
    "Pausing and stopping": {
        "keywords": ["pause", "paus", "stop", "discontinu", "closed",
                     "closure", "cancel"],
        "opportunity": "Pause-versus-stop guidance and a monthly check-in to prevent quitting (SIP Saathi topics: Thinking about pausing, Cancelling SIP).",
    },
}


def classify(text):
    """Return (best_theme, matched_keywords). Theme is None if nothing matches."""
    t = text.lower()
    hits = {name: [k for k in cfg["keywords"] if k in t] for name, cfg in THEMES.items()}
    best = max(hits, key=lambda name: len(hits[name]))
    if len(hits[best]) == 0:
        return None, []
    return best, hits[best]


rows = []
for item in EVIDENCE:
    theme, matched = classify(item["text"])
    rows.append({
        "ID": item["id"],
        "Source": item["source"],
        "Type": item["type"],
        "What it says": item["text"],
        "Theme": theme or "No clear theme",
        "Matched keywords": ", ".join(matched),
        "Link": item["url"],
    })
df = pd.DataFrame(rows)

# ------------------------------------------------------------
# 3. PAGE
# ------------------------------------------------------------
st.title("🔎 SIP Saathi Discovery Engine")
st.write(
    "Turns public feedback about SIPs into ranked product problems. "
    "It collects sources, tags each one with a theme, ranks the themes, "
    "and links every theme to a SIP Saathi feature."
)
st.caption(
    "Method: keyword scoring (rule-based), not generative AI. "
    "10 public items. These are signals to investigate, not a representative sample."
)

counts = df["Theme"].value_counts()

c1, c2, c3 = st.columns(3)
c1.metric("Sources analysed", len(df))
c2.metric("Themes found", int((counts.index != "No clear theme").sum()))
c3.metric("Top theme", counts.index[0])

st.subheader("1. Themes ranked by number of sources")
st.bar_chart(counts)

st.subheader("2. Evidence table")
st.dataframe(
    df,
    hide_index=True,
    column_config={
        "Link": st.column_config.LinkColumn("Source link", display_text="Open"),
    },
)

st.subheader("3. From theme to product opportunity")
for name, cfg in THEMES.items():
    n = int(counts.get(name, 0))
    with st.expander(f"{name}  ({n} sources)"):
        st.write(cfg["opportunity"])
        for _, r in df[df["Theme"] == name].iterrows():
            st.markdown(f"- [{r['Source']}]({r['Link']})")

st.subheader("4. Try it yourself")
st.write(
    "Paste any public comment or review about an SIP and see which theme "
    "the engine assigns."
)
sample = st.text_area(
    "Paste text here",
    placeholder="Example: My SIP payment failed and the bank charged me a penalty.",
)
if st.button("Classify this text"):
    if not sample.strip():
        st.warning("Please paste some text first.")
    else:
        theme, matched = classify(sample)
        if theme is None:
            st.info("No clear theme found. In a real workflow this would go to manual review.")
        else:
            st.success(f"Theme: {theme}")
            st.write("Matched keywords:", ", ".join(matched))
            st.write("Suggested product response:", THEMES[theme]["opportunity"])

st.caption("SIP Saathi | Independent Groww case-study prototype | Not an official Groww product")
