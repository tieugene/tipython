= PROPFIND =
Request:
	Header (Depth 0):
	Body:
====
<?xml version="1.0" encoding="utf-8"?>
<D:propfind xmlns:D="DAV:">
  <D:prop>
    <D:creationdate/>
    <D:getcontentlength/>
    <D:displayname/>
    <D:source/>
    <D:getcontentlanguage/>
    <D:getcontenttype/>
    <D:executable/>
    <D:getlastmodified/>
    <D:getetag/>
    <D:supportedlock/>
    <D:lockdiscovery/>
    <D:resourcetype/>
  </D:prop>
</D:propfind>
====
Responce (Depth: 0):
	Body:
====
<?xml version="1.0" encoding="utf-8"?>
<D:multistatus xmlns:D="DAV:" xmlns:ns0="DAV:">
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2011-04-11T04:03:09Z</lp1:creationdate>
        <D:getcontenttype>httpd/unix-directory</D:getcontenttype>
        <lp1:getlastmodified>Mon, 11 Apr 2011 04:03:09 GMT</lp1:getlastmodified>
        <lp1:getetag>"78c001-1000-4a09ca74c9940"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
</D:multistatus>
====
Responce (Depth: 1):
	Header:
	Body: a response per object (including asked)
====
<?xml version="1.0" encoding="utf-8"?>
<D:multistatus xmlns:D="DAV:" xmlns:ns0="DAV:">
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2011-04-11T04:03:09Z</lp1:creationdate>
        <D:getcontenttype>httpd/unix-directory</D:getcontenttype>
        <lp1:getlastmodified>Mon, 11 Apr 2011 04:03:09 GMT</lp1:getlastmodified>
        <lp1:getetag>"78c001-1000-4a09ca74c9940"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/Images/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2011-04-07T09:28:26Z</lp1:creationdate>
        <D:getcontenttype>httpd/unix-directory</D:getcontenttype>
        <lp1:getlastmodified>Thu, 07 Apr 2011 09:28:26 GMT</lp1:getlastmodified>
        <lp1:getetag>"7aa00f-1000-4a050bb3ce280"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/tmp/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2010-03-21T02:36:10Z</lp1:creationdate>
        <D:getcontenttype>httpd/unix-directory</D:getcontenttype>
        <lp1:getlastmodified>Sun, 21 Mar 2010 02:36:10 GMT</lp1:getlastmodified>
        <lp1:getetag>"7f021a-1000-48246717a3a80"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/Download/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2010-02-06T15:12:36Z</lp1:creationdate>
        <lp1:getlastmodified>Sat, 06 Feb 2010 15:12:36 GMT</lp1:getlastmodified>
        <lp1:getetag>"78c002-3000-47eefff848100"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:getcontenttype/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/dvd/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2009-09-13T11:34:17Z</lp1:creationdate>
        <D:getcontenttype>httpd/unix-directory</D:getcontenttype>
        <lp1:getlastmodified>Fri, 29 Jun 2007 18:45:01 GMT</lp1:getlastmodified>
        <lp1:getetag>"78c096-1000-4340fe0696540"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/justfile.txt</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2011-04-11T04:03:09Z</lp1:creationdate>
        <lp1:getcontentlength>7</lp1:getcontentlength>
        <D:getcontenttype>text/plain</D:getcontenttype>
        <lp1:getlastmodified>Mon, 11 Apr 2011 04:03:09 GMT</lp1:getlastmodified>
        <lp1:getetag>"860066-7-4a09ca74c9940"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype/>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
  <D:response xmlns:lp1="DAV:" xmlns:lp2="http://apache.org/dav/props/" xmlns:g0="DAV:">
    <D:href>/ftp/pub/</D:href>
    <D:propstat>
      <D:prop>
        <lp1:creationdate>2011-01-17T08:20:29Z</lp1:creationdate>
        <D:getcontenttype>text/html</D:getcontenttype>
        <lp1:getlastmodified>Mon, 17 Jan 2011 08:20:29 GMT</lp1:getlastmodified>
        <lp1:getetag>"a0164-1000-49a0674eccd40"</lp1:getetag>
        <D:supportedlock>
          <D:lockentry>
            <D:lockscope>
              <D:exclusive/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
          <D:lockentry>
            <D:lockscope>
              <D:shared/>
            </D:lockscope>
            <D:locktype>
              <D:write/>
            </D:locktype>
          </D:lockentry>
        </D:supportedlock>
        <D:lockdiscovery/>
        <lp1:resourcetype>
          <D:collection/>
        </lp1:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
    <D:propstat>
      <D:prop>
        <g0:getcontentlength/>
        <g0:displayname/>
        <g0:source/>
        <g0:getcontentlanguage/>
        <g0:executable/>
      </D:prop>
      <D:status>HTTP/1.1 404 Not Found</D:status>
    </D:propstat>
  </D:response>
</D:multistatus>
