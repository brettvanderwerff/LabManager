function createTimer() {
    this.running = false
    this.entered_digits = 0
    this.alarm = new Audio("/static/audio/alarm.mp3")
    this.i = 1

    this.inputNumber = function(number) {
        if (this.running == true) {
            return
        }

        if (this.entered_digits == 6 ){
            return
        }

        let display_text = document.getElementById("timer-display").innerHTML
        let display_without_colon = display_text.substring(0,2) + display_text.substring(3,5) + display_text.substring(6,8) + number
        let display_trimmed = display_without_colon.substring(1,7)
        let display_with_colon = display_trimmed.substring(0,2) + ":" + display_trimmed.substring(2,4) + ":" +  display_trimmed.substring(4,6)
        document.getElementById("timer-display").innerHTML = display_with_colon
        this.entered_digits++
        }

    this.clearDisplay = function() {

        if (this.running == true) {
            this.alarm.pause()
            this.alarm.currentTime = 0
            return
        }
        this.entered_digits = 0
        document.getElementById("timer-display").innerHTML = "00:00:00"

        }

    this.addTime = function(userTime) {
        let userTimeInMilliseconds = (userTime.split(":")[0] * 3600000) + (userTime.split(":")[1] * 60000) + (userTime.split(":")[2] * 1000)
        return new Date(Date.now() + userTimeInMilliseconds)
        }

    this.millisecondsConversion = function(milliSeconds) {
        let hours = Math.floor(milliSeconds/3600000)
        if (hours <= 9) {
            hours = "0" + hours
        }
        let minutes = Math.floor((milliSeconds - (hours * 3600000))/ 60000)
        if (minutes <= 9) {
            minutes = "0" + minutes
        }
        let seconds = Math.floor(((milliSeconds - (hours * 3600000) - (minutes * 60000))/ 1000))
        if (seconds <= 9) {
            seconds = "0" + seconds
        }
        return hours + ":" + minutes + ":" + seconds
        }



  this.timerRun = function(stopTime) {
    if (this.running == false) {
    return
    }
    let timeDelta = stopTime - Date.now()
    if (timeDelta <= 0) {
    this.alarm.play()
    return
    }
    document.getElementById("timer-display").innerHTML = this.millisecondsConversion(timeDelta)
    let _this = this
    setTimeout(function() {
        _this.timerRun(stopTime)}, 100)
    }


    this.startTimer = function() {
        this.running = true
        let input = document.getElementById("timer-display").innerHTML
        stopTime = this.addTime(input)
        this.timerRun(stopTime)
    }

    this.stopTimer = function() {
        this.running = false
        this.alarm.pause()
        this.alarm.currentTime = 0

    }

    this.updateName = function() {
        let name = document.getElementById("name-text").value
        document.getElementById("timer-name").innerHTML = name

    }


}
