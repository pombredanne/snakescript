
function map() {
    if (Array.prototype.map && arguments.length == 2) {
        var A = arguments[1];
        if (!(A instanceof Array)) {
            A = list(A);
        }
        return Array.prototype.map.call(A, arguments[0]);
    }
    var iterables = list(arguments),
        func = iterables.shift(),
        out = [];
    for (var I = iter(iterables), i = next(I); i !== undefined; i = next(I)) {
        out.push(null);
    }
    return list(out);
}

