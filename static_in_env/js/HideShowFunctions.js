function yesnoCheck(that, target) {
    if (that.value == "a") {
        document.getElementById(target).style.display = "block";
    } else {
        document.getElementById(target).style.display = "none";
    }
}

function brd(that, target) {
    if (that.value == "b") {
        document.getElementById(target).style.display = "none";
    } else {
        document.getElementById(target).style.display = "block";
    }
}
