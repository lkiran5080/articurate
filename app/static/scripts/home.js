$(document).ready(function () {
  let urlBox = $("#urlBox");
  let submitBtn = $("#submitBtn");
  let content = $("#content");
  let summary = $("#summary");
  let title = $("#title");
  let sourceUrl = $("#sourceUrl");
  let publishDate = $("#publishDate");
  let authors = $("#authors");

  let trackId = "";
  let progressInterval = "";
  let sound;
  let siriWave;

  let playBtn = $("#playBtn");
  let pauseBtn = $("#pauseBtn");
  let stopBtn = $("#stopBtn");
  let progress = $("#progress");

  submitBtn.on("click", () => {
    let url = urlBox.val();
    if (url == "") {
      alert("Please Enter a URL!");
      return 0;
    }

    console.log("url: ", url);

    submitBtn.find("i").remove();
    submitBtn.prepend(`<i class="fa fa-circle-o-notch fa-spin"></i>`);

    let data = {
      source_url: url,
    };

    console.log("POST data: ", data);

    postData("/articurate", data)
      .then((data) => {
        let submitBtn = $("#submitBtn");
        submitBtn.find("i").remove();
        submitBtn.prepend(`<i class="fa fa-solid fa-caret-right"></i>`);

        console.log("Response data: ", data);
        /* data["contents"].replace(/\n/g, "<br />"); */

        let summary_data = data["summary"];
        summary.text(summary_data);

        title.text(data["title"]);
        sourceUrl.text(data["source_url"]);
        authors.text(data["authors"]);
        publishDate.text(data["publish_date"]);

        let content_data = data["content"];
        content_data = content_data.replace(/(?:\r\n|\r|\n)/g, "<br>");
        content.html(content_data);

        let audio_file = data["audio_file"];
        // create howler js instance
        // create siriwave
        // add handlers to buttons
        let audio_url = `listen/${audio_file}`;

        let siriWave = new SiriWave({
          container: document.querySelector("#siriContainer"),
          style: "ios",
          height: 400,

          autostart: false,
          cover: true,
          speed: 0.1,
          amplitude: 1,
        });

        if (sound) {
          sound.stop();
        }
        sound = new Howl({
          src: [audio_url],
          autoplay: false,
          loop: false,
          volume: 1,
          html5: true,
        });

        playBtn.on("click", () => {
          if (trackId == "") {
            trackId = sound.play();
          } else {
            sound.play(trackId);
          }
          siriWave.start();

          progressInterval = setInterval(() => {
            let seek = sound.seek(trackId) || 0;

            let newWidth = ((seek / sound.duration()) * 100 || 0) + "%";

            progress.css("width", newWidth);
          }, 50);
        });

        pauseBtn.on("click", () => {
          sound.pause(trackId);

          clearInterval(progressInterval);
          siriWave.stop();
        });

        stopBtn.on("click", () => {
          sound.stop(trackId);

          clearInterval(progressInterval);

          progress.css("width", "0%");

          siriWave.stop();
        });
      })
      .catch((err) => {
        submitBtn.find("i").remove();
        submitBtn.prepend(`<i class="fa fa-solid fa-caret-right"></i>`);
        console.log("An error occured!", err);

        content.text("OOPS! Something went wrong...");
      })
      .finally(() => {
        $("html, body")
          .stop()
          .animate(
            {
              scrollTop: $("#summaryRow").offset().top,
            },
            1000,
            "linear"
          );
      });
  });

  urlBox.on("keyup", (event) => {
    if (event.keyCode === 13) {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      submitBtn.click();
    }
  });

  // Example POST method implementation:
  async function postData(url = "", data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }
});
