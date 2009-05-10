<%inherit file="base.mako"/>\
<%def name="head()">\
    <link rel="stylesheet" type="text/css" charset="utf-8" media="all" href="/css/nav.css">
</%def>\
<%def name="menu()">\
<div id="nav_header">
    <table>
        <tr>
            <td rowspan="2">
                <img src="/images/logo_small.png" width="100" height="109" alt="" title="">
            </td>
            <td width="100%">
                <h1>EventGhost</h1>
            </td>
            <td rowspan="2">
                <form id="donation_button" action="https://www.paypal.com/cgi-bin/webscr" method="post">
                <input type="hidden" name="cmd" value="_xclick">
                <input type="hidden" name="business" value="donations@eventghost.org">
                <input type="hidden" name="item_name" value="EventGhost donations">
                <input type="hidden" name="no_shipping" value="1">
                <input type="hidden" name="return" value="http://www.eventghost.org/forum/">
                <input type="hidden" name="cancel_return" value="http://www.eventghost.org/forum/">
                <input type="hidden" name="cn" value="Optional Comments">
                <input type="hidden" name="currency_code" value="USD">
                <input type="hidden" name="tax" value="0">
                <input type="hidden" name="lc" value="US">
                <input type="hidden" name="bn" value="PP-DonationsBF">
                <input type="image" src="http://www.eventghost.org/images/x-click-but21.gif" border="0" name="submit" alt="Make payments with PayPal - it's fast, free and secure!" style="background-color: transparent; border: 0px;">
                <img alt="" border="0" src="http://www.eventghost.org/images/pixel.gif" width="1" height="1">
                </form>
            </td>
        </tr>
	<tr  id="nav_menu_bar">
	    <td>
		<ul>
% for page in MENU_TABS:
                    <li\
% if page == CURRENT:
 id="nav_current"\
% endif
><a href="${page.target}">${page.name}</a></li>
% endfor
                </ul>
            </td>
	</tr>
    </table>
</div>
</%def>\
<%def name="footer()">\
</%def>\
${next.body()}