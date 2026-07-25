# Aura Architecture — Exploration

> Q&A format. New facts marked `<new fact>..</new fact>`. Each section ends with a question.

---

## 1. Users & Identity

**Q: Who are the users?**

A: Two roles — people recording moments (Farm users) and people receiving points (Card holders). Same person can be both.

<new fact>Users have two modes: recorder (Farm) and subject (Card). Same person, different contexts.</new fact>

**Q: How does a user prove who they are?**

A: The Card is an identification beacon. It uniquely identifies a user + their IP. Cryptographic keypair generated on-device.

<new fact>Identity = cryptographic keypair generated locally on first launch.</new fact>
<new fact>Identity is tied to IP address — same person on different network = different identity until proven otherwise.</new fact>

**Q: Can one person have multiple devices?**

A: Not yet answered.

**Q: Is identity portable across devices?**

A: Not yet answered.

**Q: What happens when IP changes (mobile, travel, VPN)?**

A: Not yet answered.

---

**→ Next question:** How does a Farm instance know which Card holder is in front of the camera?
