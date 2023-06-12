$(document).ready(function() {
  function fetchData()
  {

    $.ajax({
      url: '/data',
      method: 'GET',
      dataType: 'json',
      success: function(response) {
        // Reverse the response data array
        response.reverse();
  
        var emailTable = $('#emailTable tbody');
  
        // Clear existing table rows
        emailTable.empty();
  
        // Loop through the reversed response data and generate table rows
        $.each(response, function(index, email) {
          var row = $('<tr>');
          row.append($('<td>').text(email.id));
          row.append($('<td>').text(email.time));
          row.append($('<td>').text(email.from));
          row.append($('<td>').text(email.to));
          row.append($('<td>').text(email.subject));
          row.append($('<td>').text(email.sent));
          row.append($('<td>').text(email.model));
          row.append($('<td>').text(email.spam_score));
          row.append($('<td>').text(email.ham_score));

                  // Add flag icon with different colors based on conditions
          var predictCell = $('<td>');

          // Add flag icon with different colors based on conditions
          if (email.predict) {
            var flagIcon = $('<i>').addClass('fas fa-flag').css('color', '#fa4251');
            predictCell.append(flagIcon);
            predictCell.append('Spam');
          } else {
            var flagIcon = $('<i>').addClass('fas fa-flag').css('color', '#00b5e9');
            predictCell.append(flagIcon);
            predictCell.append('Ham');
          }
  
          row.append(predictCell);

          emailTable.append(row);
        });
      },
      error: function() {
        alert('Error occurred while retrieving data.');
      }
    });
  }
  // Function to poll data at regular intervals
  function pollData() {
    fetchData(); // Fetch data immediately
    setInterval(fetchData, 1000); // Fetch data every 5 seconds
  }

  // Start polling data
  pollData();

});
  