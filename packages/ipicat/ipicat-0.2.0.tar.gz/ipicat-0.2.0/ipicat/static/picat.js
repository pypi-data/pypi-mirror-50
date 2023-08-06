"use strict";

CodeMirror.defineMode("text/picat", function(config) {

  var isOperatorChar = /[+\-*=\@\&|\:#<>\/]/;

  var keywords = {"else":true,
  "end":true,
  "foreach":true,
  "if":true,
  "in":true,
  "then":true
  }

  var specials = {"acyclic_term":true,
  "and_to_list":true,
  "append":true,
  "apply":true,
  "arity":true,
  "array":true,
  "atom":true,
  "atom_chars":true,
  "atom_codes":true,
  "atomic":true,
  "attr_var":true,
  "between":true,
  "bind_vars":true,
  "call":true,
  "call_cleanup":true,
  "catch":true,
  "char":true,
  "chr":true,
  "clear":true,
  "compare_terms":true,
  "compound":true,
  "copy_term":true,
  "count_all":true,
  "delete":true,
  "delete_all":true,
  "different_term":true,
  "digit":true,
  "div":true,
  "dvar":true,
  "dvar_or_int":true,
//   "end":true,
  "fail":true,
  "false":true,
  "find_all":true,
  "findall":true,
  "first":true,
  "flatten":true,
  "float":true,
  "fold":true,
//   "foreach":true,
  "freeze":true,
  "get":true,
  "get_attr":true,
  "get_global_map":true,
  "get_heap_map":true,
  "get_table_map":true,
  "ground":true,
  "handle_exception":true,
  "has_key":true,
  "hash_code":true,
  "head":true,
  "heap_is_empty":true,
  "heap_pop":true,
  "heap_push":true,
  "heap_size":true,
  "heap_to_list":true,
  "heap_top":true,
  "import":true,    
//   "in":true,
  "insert":true,
  "insert_all":true,
  "insert_ordered":true,
  "insert_ordered_down":true,
  "int":true,
  "integer":true,
  "is":true,
  "keys":true,
  "last":true,
  "len":true,
  "length":true,
  "list":true,
  "list_to_and":true,
  "lowercase":true,
  "map":true,
  "map_to_list":true,
  "max":true,
  "maxint_small":true,
  "maxof":true,
  "maxof_inc":true,
  "membchk":true,
  "member":true,
  "min":true,
  "minint_small":true,
  "minof":true,
  "minof_inc":true,
  "mod":true,
  "name":true,
  "new_array":true,
  "new_list":true,
  "new_map":true,
  "new_max_heap":true,
  "new_min_heap":true,
  "new_set":true,
  "new_struct":true,
  "nonvar":true,
  "not":true,
  "notin":true,
  "nth":true,
  "number":true,
  "number_char":true,
  "number_codes":true,
  "number_vars":true,
  "once":true,
  "ord":true,
  "parse_radix_string":true,
  "parse_term":true,
  "post_event":true,
  "post_event_any":true,
  "post_event_bound":true,
  "post_event_dom":true,
  "post_event_ins":true,
  "print":true,
  "println":true,
  "prod":true,
  "put":true,
  "put_attr":true,
  "real":true,
  "reduce":true,
  "rem":true,
  "remove_dumps":true,
  "repeat":true,
  "reverse":true,
  "second":true,
  "select":true,
  "size":true,
  "slice":true,
  "sort":true,
  "sort_down":true,
  "sort_down_remove_dups":true,
  "sort_remove_dups":true,
  "sorted":true,
  "sorted_down":true,
  "string":true,
  "struct":true,
  "subsumes":true,
  "sum":true,
  "tail":true,
  "throw":true,
  "to_array":true,
  "to_atom":true,
  "to_binary_string":true,
  "to_code":true,
  "to_fstring":true,
  "to_hex_string":true,
  "to_int":true,
  "to_integer":true,
  "to_list":true,
  "to_lowercase":true,
  "to_number":true,
  "to_oct_string":true,
  "to_radix_string":true,
  "to_real":true,
  "to_string":true,
  "to_uppercase":true,
  "true":true,
  "uppercase":true,
  "values":true,
  "var":true,
  "variant":true,
  "vars":true,
  "zip":true,

  "abs":true,
  "acos":true,
  "acosh":true,
  "acot":true,
  "acoth":true,
  "acsc":true,
  "acsch":true,
  "asec":true,
  "asech":true,
  "asin":true,
  "asinh":true,
  "atan":true,
  "atan2":true,
  "atanh":true,
  "ceiling":true,
  "cos":true,
  "cosh":true,
  "cot":true,
  "coth":true,
  "csc":true,
  "csch":true,
  "e":true,
  "even":true,
  "exp":true,
  "floor":true,
  "frand":true,
  "gcd":true,
  "log":true,
  "log10":true,
  "log2":true,
  "modf":true,
  "odd":true,
  "pi":true,
  "pow":true,
  "pow_mod":true,
  "prime":true,
  "primes":true,
  "max":true,
  "random":true,
  "random2":true,
  "round":true,
  "sec":true,
  "sech":true,
  "sign":true,
  "sin":true,
  "sinh":true,
  "sqrt":true,
  "tan":true,
  "tanh":true,
  "to_degrees":true,
  "to_radians":true,
  "truncate":true,
    
 
  "xor":true};

  var punc = ":;,.(){}[]";

  function tokenBase(stream, state) {
    var ch = stream.next();
    if (ch == '"') {
      state.tokenize.push(tokenString);
      return tokenString(stream, state);
    }
    if (/[\d\.]/.test(ch)) {
      if (ch == ".") {
        stream.match(/^[0-9]+([eE][\-+]?[0-9]+)?/);
      } else if (ch == "0") {
        stream.match(/^[xX][0-9a-fA-F]+/) || stream.match(/^0[0-7]+/);
      } else {
        stream.match(/^[0-9]*\.?[0-9]*([eE][\-+]?[0-9]+)?/);
      }
      return "number";
    }
    if (ch == "/") {
      if (stream.eat("*")) {
        state.tokenize.push(tokenComment);
        return tokenComment(stream, state);
      }
    }
    if (ch == "%") {
      stream.skipToEnd();
      return "comment";
    }
    if (isOperatorChar.test(ch)) {
      stream.eatWhile(isOperatorChar);
      return "operator";
    }
    if (punc.indexOf(ch) > -1) {
      return "punctuation";
    }
    stream.eatWhile(/[\w\$_\xa1-\uffff]/);
    var cur = stream.current();
    if (keywords.propertyIsEnumerable(cur)) {
      return "keyword";
    }
    return "variable";
  }

  function tokenComment(stream, state) {
    var maybeEnd = false, ch;
    while (ch = stream.next()) {
      if (ch == "/" && maybeEnd) {
        state.tokenize.pop();
        break;
      }
      maybeEnd = (ch == "*");
    }
    return "comment";
  }

  function tokenUntilClosingParen() {
    var depth = 0;
    return function(stream, state, prev) {
      var inner = tokenBase(stream, state, prev);
      console.log("untilClosing",inner,stream.current());
      if (inner == "punctuation") {
        if (stream.current() == "(") {
          ++depth;
        } else if (stream.current() == ")") {
          if (depth == 0) {
            stream.backUp(1)
            state.tokenize.pop()
            return state.tokenize[state.tokenize.length - 1](stream, state)
          } else {
            --depth;
          }
        }
      }
      return inner;
    }
  }

  function tokenString(stream, state) {
    var escaped = false, next, end = false;
    while ((next = stream.next()) != null) {
      if (next=='(' && escaped) {
        state.tokenize.push(tokenUntilClosingParen());
        return "string";
      }
      if (next == '"' && !escaped) {end = true; break;}
      escaped = !escaped && next == "\\";
    }
    if (end || !escaped)
      state.tokenize.pop();
    return "string";
  }

  return {
    startState: function(basecolumn) {
      return {
        tokenize: []
      };
    },

    token: function(stream, state) {
      if (stream.eatSpace()) return null;
      var style = (state.tokenize[state.tokenize.length - 1] || tokenBase)(stream, state);
      console.log("token",style);
      return style;
    },

    blockCommentStart: "/*",
    blockCommentEnd: "*/",
    lineComment: "%"
  };
});

CodeMirror.defineMIME("text/picat", "text/picat");

Jupyter.CodeCell.options_default.highlight_modes['magic_text/picat'] = {'reg':[/^%%picat/]} ;

Jupyter.notebook.get_cells().map(function(cell){
  if (cell.cell_type == 'code'){ cell.auto_highlight(); }
}) ;