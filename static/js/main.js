$(document).ready(function() {
	rangeSlider();
	autocompleteHandler($("#messagebox"));
});

// Borrowed from https://codepen.io/seanstopnik/pen/CeLqA
var rangeSlider = function(){
	var slider = $('.range-slider'),
		range = $('.range-slider__range'),
		value = $('.range-slider__value');

	slider.each(function(){
		value.each(function(){
			var value = $(this).prev().attr('value');
			$(this).html(value);
		});

		range.on('input', function(){
			$(this).next(value).html(this.value);
		});
	});
};

// Adapted from https://www.w3schools.com/howto/howto_js_autocomplete.asp
function autocompleteHandler(inp) {
	var currentFocus;

	// Execute when someone writes in the text field:
	inp.on("input", function(e) {
		var target = $(e.currentTarget);
		var val = target.val();
		if (!val) {
			closeAllLists();
			return false;
		}
		// Fetch the user's choice of max results
		max_results = $('#range-slider').val();
		// Send a get request to fetch autocomplete results
		var request = 'http://localhost:13000/autocomplete';
		var params = {'query': val, 'max_results': max_results};
		$.get(request, params, function (response) {
			fillResults(target, response['Completions']);
		});
	});

	// Allow navigating results with keyboard
	inp.keydown(function(e) {
		var target = $(e.currentTarget);
		var list = $("#" + target.attr('id') + "autocomplete-list");
		if (list) {
			list = list.find("div");
		}
		switch(e.which) {
			case 40:
				// Down arrow key
				currentFocus++;
				addActive(list);
				break;
			case 38:
				// Up arrow key
				currentFocus--;
				addActive(list);
				break;
			case 13:
				// Enter key
				e.preventDefault();
				if (currentFocus > -1) {
					// Select the active result
					if (list) {
						list.get(currentFocus).click();
					}
				}
				break;
			default:
				break;
		}
	});

	function fillResults(inp, results) {
		// close any already open lists of autocompleted values
		closeAllLists();
		currentFocus = -1;
		var container = inp.parent();
		// Create div element to be a list of all autocomplete results
		container.append("<div></div");
		var list = container.children().last();
		list.attr('id', inp.attr('id') + "autocomplete-list");
		list.addClass("autocomplete-items");
		results.forEach(function(result) {
			// Add the result to the list
			list.append("<div></div>");
			var resultDiv = list.children().last();
			resultDiv.html(result);
			resultDiv.append("<input type='hidden' value='" + result + "'>");
			resultDiv.click(function(e) {
				inp.val($(e.currentTarget).find("input").first().val());
				// Close open autocomplete lists
				closeAllLists();
			});
		});
	}

	function addActive(list) {
		// a function to classify an item as "active"
		if (!list) {
			return false;
		}
		// start by removing the "active" class on all items
		removeActive(list);
		if (currentFocus >= list.length) {
			currentFocus = 0;
		}
		if (currentFocus < 0) {
			currentFocus = list.length - 1;
		}
		$(list.get(currentFocus)).addClass("autocomplete-active");
	}

	function removeActive(list) {
		// a function to remove the "active" class from all autocomplete items
		list.each(function(index, item) {
			$(item).removeClass("autocomplete-active");
		});
	}

	function closeAllLists(elem) {
		// close all autocomplete lists in the document, except elem
		var lists = $(".autocomplete-items");
		lists.each(function(index, list) {
			if (elem != list && elem != inp) {
				list.remove();
			}
		});
	}
	
	// Close autocomplete lists when user clicks elsewhere in document
	$(document).click(function(e) {
		closeAllLists(e.currentTarget);
	});
}