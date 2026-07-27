# First Real-World Event — Guide & Checklist

> **Status:** Ready for founder action
> **Blocked on:** Founder to schedule and run the event

## Event Design

Keep it simple. The goal is to test the core flow end-to-end, not to produce a viral moment.

**Ideal format:** A casual gathering of 5-10 people for 1-2 hours. Dinner, drinks, park hangout, game night — anything where people are interacting naturally.

## Pre-Event Checklist

- [ ] **Confirm attendees.** 5+ people who have installed the app and created their Card.
- [ ] **Test the app on your own device.** Do a dry run: record → attribute → claim → check feed. Fix anything broken before the event.
- [ ] **Charge your phone.** And bring a battery pack. The Farm uses the camera.
- [ ] **Brief attendees on the mechanic.** One sentence: "When you see someone do something notable, open the Farm, record it, and give them points."
- [ ] **Set the vibe.** This is a test, not a competition. Points are fake. Have fun with it.

## During the Event

### What to observe:
- Do people naturally pull out their phones to record?
- What kinds of moments do they consider "point-worthy"?
- Does anyone try to game it? (Recording themselves, colluding, etc.)
- How does the feed feel? Is it fun to scroll through?
- Do people confirm/challenge each other's attributions?

### What to prompt (if people aren't using it):
- "Hey, that was a great joke — someone should give [name] points for that."
- "Who's winning right now? Check the feed."
- "Did anyone record [moment that just happened]?"

### What NOT to do:
- Don't force it. If people aren't into it, that's data.
- Don't explain the architecture. Nobody cares about telemetry correlation.
- Don't debug live unless it's a showstopper. Note bugs, fix later.

## Post-Event

- [ ] **Collect feedback within 24 hours** (while it's fresh). Use the template below.
- [ ] **Check the backend.** Did all attributions sync? Any errors in logs?
- [ ] **Note every bug and rough edge.** Prioritize by how many people hit it.
- [ ] **Write a post-mortem.** What worked, what didn't, what surprised you.

## Feedback Template

Send to each attendee:

```
Hey! Thanks for testing Aura today. Three quick questions:

1. What was the most fun part?
2. What was confusing or annoying?
3. Would you use this again? Why or why not?

No wrong answers. Brutal honesty appreciated.
```

## Success Looks Like

- At least 3 people used the Farm to record and attribute points
- At least 3 people checked their Card feed
- The end-to-end flow worked (record → upload → validate → claim → feed)
- You have a list of bugs and UX issues to fix
- At least one person said "this is actually cool"
