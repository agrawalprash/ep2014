var app = angular.module('DemoApp', ['jigna']);

app.controller('DemoController', function($scope){
    $scope.active_example = 0;
    $scope.active_mode = 'presentation';

    $scope.update_active_example = function(index){
        $scope.active_example = index;
    };

    $scope.update_active_mode = function(mode){
        $scope.active_mode = mode;
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

app.directive('revealWhen', function(){
    return function(scope, element, attrs){

        scope.$watch(attrs.revealWhen, function(condition){
            if (condition) {
                Reveal.layout();
            }
        });
    };
});
