# -*- coding:utf-8 -*-

import robot
from Selenium2Library import *
import sys, time, re, os

reload(sys)
sys.setdefaultencoding('utf8')

#set default timeout
TIMEOUT=15

class SeleniumExtend(Selenium2Library):

    ROBOT_LIBRARY_SCOPE = 'Global'
    localDate = time.strftime("%Y-%m-%d", time.localtime())

    def __init__(self):
        Selenium2Library.__init__(self)

    def input_until_no_error(self, locator, text, message="", timeout=TIMEOUT): 
        """Try types the given `text` into text field identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the input success.
        
        Examples:
        | Input Until No Error | css=.input_search | GitHub |              |     |
        | Input Until No Error | css=.input_search | GitHub | input GitHub | 10s |
        """
        if not message:
            message = "Typing text '%s' into text field '%s'" % (text, locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.input_text, locator, text)
    
    def click_until_no_error(self, locator, message="", timeout=TIMEOUT):
        """Try click element identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | Click Until No Error | css=.btn |           |     |
        | Click Until No Error | css=.btn | click btn | 10s |
        """
        if not message:
            message = "Clicking element '%s'" % locator
        self._wait_until_no_error_fixed(timeout, True, message, self.click_element, locator)
    
    def click_nth_element(self, locator, nth=1):
        """Click the nth element identified by `locator`.
        
        Examples:
        | #Click the 2th element |          |    |
        | Click Nth Element      | css=.btn |  2 |
        | #Click last element    |          |    |
        | Click Nth Element      | css=.btn | -1 |
        """
        try:
            nth = int(nth)
        except ValueError, e:
            raise ValueError(u"'%s' is not a number" % (nth))
        if nth == 0:
            raise ValueError(u"'nth' must not equal 0")
        elements = self.get_webelements(locator)
        self._info("Clicking %dth element '%s'" % (nth, locator))
        if nth > 0:
            elements[nth-1].click()
        elif nth < 0:
            elements[nth].click()
        
    def click_nth_until_no_error(self, locator, nth=1, message="", timeout=TIMEOUT):
        """Click the nth element identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | #Click the 2th element   |          |    |                |     |
        | Click Nth Until No Error | css=.btn | 2  |                |     |
        | #Click last element      |          |    |                |     |
        | Click Nth Until No Error | css=.btn | -1 | click last btn | 10s |
        
        """
        if not message:
            message = "Clicking %sth element '%s'" % (nth, locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.click_nth_element, locator, nth)
        
    def click_until_element_exists(self, locator, wait_locator, message="", timeout=TIMEOUT):
        """Click element identified by `locator` until element identified by `wait_locator` appear.
        
        Fails if `timeout` expires before element identified by `wait_locator` appear.
        
        Examples:
        | Click Until Element Exists | id=first | id=twice |                                    |     |
        | Click Until Element Exists | id=first | id=twice | Click 'first' until 'twice' appear | 10s |
        """
        if not message:
            message = "Clicking element '%s' until element '%s' appear" % (locator, wait_locator)
        def click_if_not_exists():
            try:
                self.click_element(locator)
            except:
                pass
            self.page_should_contain_element(wait_locator)
        self._wait_until_no_error_fixed(timeout, True, message, click_if_not_exists)
    
    def click_nth_until_element_exists(self, locator, nth, wait_locator, message="", timeout=TIMEOUT):
        """Click the nth element identified by `locator` until element identified by `wait_locator` appear.
        
        Fails if `timeout` expires before element identified by `wait_locator` appear.
        
        Examples:
        | Click Nth Until Element Exists | id=test1 |  2 | id=test2 |                                         |     |
        | Click Nth Until Element Exists | id=test1 | -1 | id=test2 | Click last 'test1' until 'test2' appear | 10s |
        """
        if not message:
            message = "Clicking %sth element '%s' until element '%s' appear" % (nth, locator, wait_locator)
        def click_nth_if_not_exists():
            try:
                self.click_nth_element(locator, nth)
            except:
                pass
            self.page_should_contain_element(wait_locator)
        self._wait_until_no_error_fixed(timeout, True, message, click_nth_if_not_exists)
        
    def click_element_js(self, locator_css):
        """JavaScript click element identified by `locator_css`.
        
        Examples:
        | Click Element Js | css=.btn |
        """
        locator_css = self._format_css(locator_css)
        js = 'document.querySelector("'+ locator_css + '").click()'
        self._info("JavaScript clicking element '%s'" % (locator_css))
        self._current_browser().execute_script(js)
    
    def click_until_no_error_js(self, locator_css, message="", timeout=TIMEOUT):
        """Try JavaScript click element identified by `locator_css` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | Click Until No Error Js | css=.btn |                      |     |
        | Click Until No Error Js | css=.btn | JavaScript click btn | 10s |
        """
        if not message:
            message = "JavaScript clicking element '%s'" % locator_css
        self._wait_until_no_error_fixed(timeout, True, message, self.click_element_js, locator_css)
        
    def click_if_exists_in_time(self, locator, message="", timeout=TIMEOUT):
        """Try click element identified by `locator` in setting time.
        
        Ignore if `timeout` expires before the click success.
        
        Examples:
        | Click If Exists In Time | css=.btn |                                   |     |
        | Click If Exists In Time | css=.btn | click btn, no error if click fail | 10s |
        """
        if not message:
            message = "Clicking element '%s'" % locator
        self._wait_until_no_error_fixed(timeout, False, message, self.click_element, locator)

    def click_if_exists_in_time_js(self, locator_css, message="", timeout=TIMEOUT):
        """Try JavaScript click element identified by `locator_css` in setting time.
        
        Ignore if `timeout` expires before the JavaScript click success.
        
        Examples:
        | Click If Exists In Time Js | css=.btn |                                              |     |
        | Click If Exists In Time Js | css=.btn | JavaScript click btn, no error if click fail | 10s |
        """
        if not message:
            message = "JavaScript clicking element '%s'" % locator_css
        self._wait_until_no_error_fixed(timeout, False, message, self.click_element_js, locator_css)
        
    def double_click_until_no_error(self, locator, message="", timeout=TIMEOUT):  
        """Try double click element identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | Double Click Until No Error | link=Login |                         |     |
        | Double Click Until No Error | link=Login | double click login link | 10s |
        """
        if not message:
            message = "Double clicking element '%s'" % locator
        self._wait_until_no_error_fixed(timeout, True, message, self.double_click_element, locator)
        
    def select_window_until_no_error(self, locator, message="", timeout=TIMEOUT):
        """Try selects the window matching locator and return previous window handle until no error occurred. 
        
        locator: any of name, title, url, window handle, excluded handle's list, or special words.
        
        Examples:
        | Select Window Until No Error | Explore · GitHub |                               |     |
        | Select Window Until No Error | Explore · GitHub | change to Explore GitHub page | 10s |
        """
        if not message:
            message = "Selecting window '%s'" % locator
        self._wait_until_no_error_fixed(timeout, True, message, self.select_window, locator)
    
    def choose_file_until_no_error(self, locator, file_path, message="", timeout=TIMEOUT):
        """Try inputs the `file_path` into file input field found by `locator` until no error occurred. 
        
        Fails if `timeout` expires before the choose file success.
        
        Examples:
        | #Absolute file path                |                  |             |             |     |
        | Choose File Until No Error         | css=.upload_file | d:/file.txt | upload file | 10s |
        | #Relative file path to os.getcwd() |                  |             |             |     |
        | Choose File Until No Error         | css=.upload_file | file.txt    |             |     |
        """
        file_path = file_path.encode("utf-8") if os.path.isabs(file_path) else os.path.abspath(file_path.encode("utf-8"))
        if not os.path.exists(file_path):
            raise ValueError(u"path file '%s' is not exists." % file_path)
        if not message:
            message = "Choosing file '%s' from button '%s'" % (file_path, locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.choose_file, locator, file_path)
    
    def execute_javascript_until_no_error(self, js_code, message="", timeout=TIMEOUT):
        """Try executes the given JavaScript code until no error occurred.
        
        Fails if `timeout` expires before the execute JavaScript success.
        
        Examples:
        | Execute JavaScript Until No Error | document.querySelector('.btn').click() |                      |     |
        | Execute JavaScript Until No Error | document.querySelector('.btn').click() | javascript click btn | 10s |
        """
        if not message:
            message = "Executing JavaScript: %s" % js_code
        self._wait_until_no_error_fixed(timeout, True, message, self._current_browser().execute_script, js_code)
    
    def select_radio_button_until_no_error(self, group_name, value, message="", timeout=TIMEOUT):
        """Try sets selection of radio button group identified by `group_name` to `value` until no error occurred.
        
        Fails if `timeout` expires before the select success.
        Only support JavaScript radio button widget.
        
        Examples:
        | Select Radio Button Until No Error | radio_name | 1 |                |     |
        | Select Radio Button Until No Error | radio_name | 1 | select radio 1 | 10s |
        """
        if not message:
            message = "Selecting '%s' from radio button '%s'" % (value, group_name)
        self._wait_until_no_error_fixed(timeout, True, message, self.select_radio_button, group_name, value)
    
    def select_from_list_until_no_error(self, locator, item_list, message="", timeout=TIMEOUT):
        """Try selects `item` from list identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the select success.
        Only support JavaScript select widget.
        
        Examples:
        | Select From List Until No Error | id=nr   | 10      |                  |     |
        | Select From List Until No Error | css=.nr | [10,20] | select 10 and 20 | 10s |
        """
        if not isinstance(item_list, list):
            item_list = self._convert_to_list(item_list)
        if not message:
            message = "Selecting '%s' from list '%s'" % (str(item_list), locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.select_from_list, locator, *item_list)
    
    def is_element_present(self, locator):
        """Check the element identified by `locator` is exist or not. 
        
        Return True if locator element present, False if locator element not present.
        
        Examples:
        | ${isPresent}= | Is Element Present | css=.btn |
        """
        return self._is_element_present(locator)
    
    def get_element_count(self, locator):
        """Count elements found by `locator`.
        
        Examples:
        | ${count}= | Get Element Count | css=.btn |
        """
        return len(self.get_webelements(locator))

    def get_element_count_in_time(self, locator, message="", timeout=TIMEOUT):
        """Count elements found by `locator` until result is not 0.
        
        Return 0 if `timeout` expires.
        
        Examples:
        | ${count}= | Get Element Count In Time | css=.btn |              |     |
        | ${count}= | Get Element Count In Time | css=.btn | cout element | 10s |
        """
        return self._wait_until_not_value(timeout, 0, False, message, self.get_element_count, locator)

    def get_element_count_in_time_js(self, locator_css, message="", timeout=TIMEOUT):
        """JavaScript count elements found by `locator_css` until result is not 0.
        
        Return 0 if `timeout` expires.

        Examples:
        | ${count}= | Get Element Count In Time Js | css=.btn |                          |     |
        | ${count}= | Get Element Count In Time Js | css=.btn | JavaScript count element | 10s |
        """
        locator_css = self._format_css(locator_css)
        js = "return document.querySelectorAll('" + locator_css + "').length"
        return self._wait_until_not_value(timeout, 0, False, message, self._current_browser().execute_script, js)
 
    def js_set_attr(self, locator_css, attribute, value):
        """Set value of attribute for element what `locator_css` located.
        
        Examples:
        | Js Set Attr | css=.ll_choose | class | .ll_choose hover |
        """
        locator_css = self._format_css(locator_css)
        js = "document.querySelector('%s').setAttribute('%s','%s')" % (locator_css, attribute, value)
        self._current_browser().execute_script(js)
    
    def js_remove_attr(self, locator_css, attribute):
        """Remove value of attribute for element what locator_css located.
        
        Examples:
        | Js Remove Attr | css=.datewidget | readOnly |
        """
        js = "document.querySelector('%s').removeAttribute('%s')" % (locator_css, attribute)
        self._current_browser().execute_script(js)
 
    def set_date_js(self, locator_css, datestring = None):
        """Set the date of date widget by `locator_css`. date string should like 'YYYYMMDD','YYYY-MM-DD','YYYY/MM/DD'.
        
        Using current date if datestring is None.
        Only support JavaScript date widget.
        
        Examples:
        | Set Date Js         | css=.datewidget | 2016-01-01 |
        | #Using current date |                 |            |
        | Set Date Js         | css=.datewidget |            |
        """
        if datestring is not None:
            if len(datestring) < 8 or re.search('[^0-9-/]', datestring):
                raise ValueError(u"date string should like 'YYYYMMDD','YYYY-MM-DD','YYYY/MM/DD'")           
            if re.search('[-/]', datestring) is None:
                datestring = datestring[0:4] + '-' + datestring[4:6] + '-' + datestring[6:8]
                print datestring
            else:
                datestring = datestring.replace('/','-')
        else:        
            datestring = self.localDate
        self.js_remove_attr(locator_css, "readOnly")
        self.js_set_attr("value", datestring)
    
    def page_should_contain_text_in_time(self, text, message="", timeout=TIMEOUT):
        """Verifies text is found on the current page in setting time.
        
        Fails if `timeout` expires before find page contain text.
        
        Examples:
        | Page Should Contain Text In Time | Sign up for GitHub |                 |     |
        | Page Should Contain Text In Time | Sign up for GitHub | check home page | 10s |
        """
        if not message:
            message = "Page should have contained text '%s' in %s" % (text, self._format_timeout(timeout))
        self._wait_until_no_error_fixed(timeout, True, message, self.page_should_contain, text, 'NONE')

    def page_should_contain_element_in_time(self, locator, message="", timeout=TIMEOUT):
        """Verifies element identified by `locator` is found on the current page in setting time.
        
        Fails if `timeout` expires before find page contain locator element.
        
        Examples:
        | Page Should Contain Element In Time | id=loginBtn |                          |     |
        | Page Should Contain Element In Time | id=loginBtn | check login button exist | 10s |
        """
        if not message:
            message = "Page should have contained element '%s' in %s" % (locator, self._format_timeout(timeout))
        self._wait_until_no_error_fixed(timeout, True, message, self.page_should_contain_element, locator, '', 'NONE')
    
    def page_should_visible_element_in_time(self, locator, message="", timeout=TIMEOUT):
        """Verifies element identified by `locator` is visible on the current page in setting time.
        
        Fails if `timeout` expires before find page visible locator element.
        
        Examples:
        | Page Should Visible Element In Time | id=loginBtn |                            |     |
        | Page Should Visible Element In Time | id=loginBtn | check login button visible | 10s |
        """
        if not message:
            message = "Page should visible element '%s' in %s" % (locator, self._format_timeout(timeout))
        def check_visibility():
            if self._is_visible(locator) is not True:
                raise AssertionError(message)
        self._wait_until_no_error_fixed(timeout, True, message, check_visibility)
        
    def page_should_not_visible_element_in_time(self, locator, message="", timeout=TIMEOUT):
        """Verifies element identified by `locator` is not visible on the current page in setting time.
        
        Fails if `timeout` expires before find page not visible locator element.
        
        Examples:
        | Page Should Not Visible Element In Time | id=loginBtn |                                |     |
        | Page Should Not Visible Element In Time | id=loginBtn | check login button not visible | 10s |
        """
        if not message:
            message = "Page should not visible element '%s' in %s" % (locator, self._format_timeout(timeout))
        def check_hidden():
            if self._is_visible(locator) is not False:
                raise AssertionError(message)
        self._wait_until_no_error_fixed(timeout, True, message, check_hidden)        
        
    def title_should_contain(self, *title_piece):
        """Verifies that current title contains `title_piece`.
        
        Examples:
        | Title Should Contain | GitHub | Hello | World |
        """
        title = self.get_title()
        for expected in title_piece:
            if None == re.search(expected, title):
                raise AssertionError(u"Title should contain '%s' but was '%s'" % (expected, title))
        self._info("Page title is '%s'." % (title))  
    
    def title_should_contain_in_time(self, title_piece_list, message="", timeout=TIMEOUT):
        """Verifies that current title contains `title_piece_list` in setting time.
        
        Fails if `timeout` expires before find page contains `title_piece_list`.
        
        Examples:
        | Title Should Contain In Time | GitHub, Hello, World   |             |     |
        | Title Should Contain In Time | [GitHub, Hello, World] | Check Title | 10s |
        """
        if not isinstance(title_piece_list, list):
            piece_list = self._convert_to_list(title_piece_list)
        if not message:
            message = "Title should contain '%s' in %s" % (title_piece_list, self._format_timeout(timeout))
        self._wait_until_no_error_fixed(timeout, True, message, self.title_should_contain, *piece_list)

    def wait_until_page_contains_elements(self, locator_list, message="", timeout=TIMEOUT):
        """Waits until any element specified with `locator_list` appears on current page.

        Fails if `timeout` expires before the element appears.
        
        Examples:
        | Wait Until Page Contains Elements | name=unlogin, name=login   |                      |     |
        | Wait Until Page Contains Elements | [name=unlogin, name=login] | wait elements appear | 10s |
        """
        if not isinstance(locator_list, list):
            _locator_list = self._convert_to_list(locator_list)
        message_info = "Wait Page contains %s in %s" % (" or ".join(["'"+i+"'" for i in _locator_list]), self._format_timeout(timeout))
        if not message:
            message = message_info
        self._info(u"%s." % (message_info))
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else 15
        maxtime = time.time() + timeout
        while True:
            for locator in _locator_list:
                if self._is_element_present(locator):
                    self._info(u"%s ==> PASS." % (message))
                    break
            else:
                if time.time() > maxtime:
                    raise AssertionError(u"%s ==> FAIL." % (message))
                    time.sleep(0.5)  
                continue
            break
        
    def _format_css(self, locator_css):
        eq = locator_css.find('=')
        if eq != -1:
            if locator_css[0:eq].strip().lower() == "css":
                return locator_css[eq+1:].strip()
        return locator_css.replace("\"", "'")
    
    def _convert_to_list(self, str_list):
        if str_list.startswith('[') and str_list.endswith(']'):
            str_list = str_list[1:-1]
        return [i.strip() for i in str_list.split(',')]
    
    def _wait_until_no_error_fixed(self, timeout, fail_raise_error, message, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else 15
        maxtime = time.time() + timeout
        while True:
            try:
                res = wait_func(*args)
            except Exception, e:
                timeout_error = True
            else:
                timeout_error = False
            if not timeout_error:
                self._info(u"%s ==> PASS." % (message))
                return res
            if time.time() > maxtime:
                if not fail_raise_error:
                    self._info(u"%s ==> NOT PASS." % (message))
                    break
                else:
                    raise AssertionError(u"%s ==> FAIL." % (message))
                    break
            time.sleep(0.5)
    
    def _wait_until_not_value(self, timeout, value, fail_raise_error, message, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else 15
        maxtime = time.time() + timeout
        while True:
            res = wait_func(*args)
            if res != value:
                if message:
                    self._info(u"%s ==> %s." % (message, res))
                return res
            if time.time() > maxtime:
                if not fail_raise_error:
                    if message:
                        self._info(u"%s ==> %s." % (message, res))
                    return res
                if message:
                    raise AssertionError(u"%s ==> %s." % (message, res))
                else:
                    raise AssertionError(u"Return ==> %s." % (res))
                break
            time.sleep(0.5)
