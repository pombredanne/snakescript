
//slice
function Slice(x,y,z){var N=null;if(y==N){y=x;x=N}this.step=z==N?N:z;this.start=x==N?N:x;this.stop=y==N?N:y}
(function(P){
P.indices=function(L){var N=null,x,y,z;if(L==N)throw TypeError;z=this.step==N?1:this.step;if(this.start==N)x=z<0?L-1:0;else{x=this.start;if(x<0)x+=L}if(this.stop==N)y=z<0?-1:L;else{y=this.stop;if(y<0)y+=L}return tuple([x,y,z])}
})(Slice.prototype);

