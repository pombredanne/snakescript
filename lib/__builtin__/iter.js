
function $keys(obj) {
    if (isinstance(obj, Object)) {
        var keys = [];
        for (var key in obj) {
            keys.push(key);
        }
        return keys;
    } else {
        throw TypeError("Cannot unzip non-object")
    }
}

function iter(obj, sentinel) {
    if (obj.__iter__) {
        return obj.__iter__();
    }
    if (!(obj instanceof Array)) {
        obj = $keys(obj);
    }
    var i = 0,
        NEXT = function() {
            if (i < obj.length) {
                return obj[i++];
            } else {
                return undefined;
            }
        },
        ITER = {
            __iter__: function() { return ITER },
            __next__: NEXT,
            next: NEXT
        };
    return ITER;
}

function next(iterator, d){
    var x = iterator.__next__()
    if (x === undefined) return d
    else return x
}

