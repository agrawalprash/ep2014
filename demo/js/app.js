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

        var escapeHTML = function(element) {
            var unescaped_html = element.html();
            element.text(unescaped_html).html();
        };

        scope.$watch(attrs.highlight, function(code){
            if (code.length) {
                element.html(code);
                escapeHTML(element);
                hljs.highlightBlock(element[0]);
            }
        });
    };
});
