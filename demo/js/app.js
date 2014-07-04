var app = angular.module('DemoApp', ['jigna']);

app.controller('DemoController', function($scope){
    $scope.active_example = 0;
    $scope.active_mode = 'examples';

    $scope.update_active_example = function(index){
        $scope.active_example = index;
    };
});
