This is a PyTem Template it will output these two initial lines with
{#} and {#DATE} followed by a greeting followed by four numbered lines.
% count = 10
<%greeting%> to you, <% name.upper() %>. How are you?
%    for ix in range(count):
This is line #<% ix %>.
%    end
In 5b we're here: {#}
