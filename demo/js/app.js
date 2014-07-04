var app = angular.module('DemoApp', ['jigna']);

app.controller('DemoController', function($scope){
    $scope.active_example = 0;
    $scope.active_mode = 'examples';

    $scope.update_active_example = function(index){
        $scope.active_example = index;
    };
});

app.directive('highlight', function(){
    return function(scope, element, attrs){

         var entityMap = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': '&quot;',
            "'": '&#39;',
            "/": '&#x2F;'
          };

          function escapeHtml(string) {
            return String(string).replace(/[&<>"'\/]/g, function (s) {
              return entityMap[s];
            });
          }

        scope.$watch(attrs.highlight, function(code){
            if (code.length) {
                element.html(escapeHtml(code));
                hljs.highlightBlock(element[0]);
            }
        });
    };
});
