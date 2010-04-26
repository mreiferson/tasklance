function onKeyPress(e, keycode, fnc, param) {
    var pK = e.charCode || e.keyCode;

    if(pK == keycode) {
        fnc(param);
        return false;
    }

    return true;
}

function entFunc(e, fnc, param) {
    return onKeyPress(e, 13, fnc, param);
}

function entSub(e, frm) {
    return entFunc(e, function() { frm.submit(); });
}
