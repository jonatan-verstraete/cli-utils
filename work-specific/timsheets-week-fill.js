(async () => {
  const description = "- FT/13654 annotations in the 3d viewer";
  const subjects = "Feature Development";
  const startTime = "09:00";
  const endTime = "17:00";

  /**
   * INERT START DATE HERE
   */
  let start = "";
  /**
   * INSET END DATE HERE
   */
  let end = "";

  start = new Date(start || document.querySelector("#fromDate")?.value);
  end = new Date(end || document.querySelector("#toDate")?.value);

  start.setUTCHours(0, 0, 0, 0);
  end.setUTCHours(0, 0, 0, 0);

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms * 1000));
  function eachWeekdayOfInterval({ start, end }) {
    const weekdays = [];
    let currentDate = new Date(start);
    while (currentDate <= end) {
      const dayOfWeek = currentDate.getDay();
      if (dayOfWeek >= 1 && dayOfWeek <= 5) {
        weekdays.push(new Date(currentDate));
      }
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return weekdays;
  }

  const allDates = eachWeekdayOfInterval({ start, end });
  const nrDates = allDates.length;

  //   if (!window.confirm(`Fill in "${nrDates}", days? Fyi: filter logs on "DEV"`)) {
  //     return;
  //   }
  let i = -1;
  while (i <= nrDates) {
    i++;
    const day = allDates[i];

    if (
      document
        .querySelector(`#event > tbody > tr:nth-child(${day.getDay() - 1})`)
        ?.querySelector(".viewIcon")
    ) {
      continue;
    }

    document.querySelector(`#newEventButton`).click();
    await sleep(0.02);

    document
      .querySelector("#confirmBox")
      ?.querySelector("#alertDeleteYes")
      ?.click();

    document.querySelector("input[name=eventStartTime]").value = startTime;
    document.querySelector("input[name=eventEndTime]").value = endTime;
    document.querySelector("input[name=eventSubject]").value = subjects;
    document.querySelector("textarea[name=eventDescription]").value =
      description;

    const strDay = day
      .toLocaleDateString("nl-NL")
      .split("-")
      .reverse()
      .map((i) => (i.length == 1 ? `0${i}` : i))
      .join("-");

    document.querySelector("input[name=eventStartDate]").value = strDay;
    document.querySelector("input[name=eventEndDate]").value = strDay;

    document.querySelector(`#saveEventButton`).click();

    await sleep(0.02);

    // go to next week
    // if (day >= 5 && i <= nrDates) {
    //   document.querySelector(`#nextWeek`).click();
    //   await sleep(0.2);
    // }
  }
})();
