
$class(window, "dict", [], function() {

    $def(this, "__init__", function(self, arg) {
        self.clear();
        if (arg instanceof Array) {
            for (var i = 0, len = arg.length; i < len; ++i) {
                self.$K.push(arg[i][0]);
                self.$KV[arg[i][0]] = arg[i][1];
            }
        } else {
            for (var I = iter(arg), i = next(I); i !== undefined; i = next(I)) {
                self.$K.push(i);
                self.$KV[i] = $getitem(arg, i);
            }
        }
    });
    
    $def(this, "__len__", function(self) {
        return self.$K.length;
    });
    
    $def(this, "__getitem__", function(self, index) {
        return self.$KV[index];
    });
    
    $def(this, "__iter__", function(self) {
        return iter(self.$K);
    });
    
    $def(this, "clear", function(self) {
        self.$K = [];
        self.$KV = {};
    });
    
    $def(this, "copy", function(self) {
        return dict(self.$KV);
    });
    
    $def(this, "get", function(self, key, default_) {
        if ($in(self.$K, key)) {
            return self.$KV[key];
        } else if (default_ === undefined) {
            return None;
        } else {
            return default_;
        }
    });
    
    $def(this, "items", function(self) {
        var I = [], key;
        for (var i = 0, len = self.$K.length; i < len; ++i) {
            key = self.$K[i];
            I.push(tuple([key, self.$KV[key]]));
        }
        return list(I);
    });
    
    $def(this, "keys", function(self) {
        return list(self.$K);
    });
    
    $def(this, "values", function(self) {
        var V = [];
        for (var i = 0, len = self.$K.length; i < len; ++i) {
            V.push(self.$KV[self.$K[i]]);
        }
        return list(V);
    });

});

