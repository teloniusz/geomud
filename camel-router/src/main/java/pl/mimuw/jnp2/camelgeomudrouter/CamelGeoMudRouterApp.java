package pl.mimuw.jnp2.camelgeomudrouter;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import org.apache.camel.builder.DataFormatClause;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.component.jackson.JacksonDataFormat;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.apache.camel.model.rest.RestBindingMode;
import org.apache.camel.spi.DataFormat;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import javax.naming.Context;
import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.*;
import javax.naming.ldap.LdapContext;
import javax.xml.transform.sax.SAXResult;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.concurrent.atomic.AtomicLong;

@SpringBootApplication
public class CamelGeoMudRouterApp {
    public static void main(String[] args) {
        SpringApplication.run(CamelGeoMudRouterApp.class, args);
    }

    @Component
    class GeoMudRoute extends RouteBuilder {
        @Value("${servers.auth}")
        private String authAddress;
        @Value("${servers.auth.people}")
        private String authPeopleDir;
        @Value("${servers.auth.group}")
        private String authGroup;

        public String doAuth(HashMap<String, String> data) {
            String user = data.getOrDefault("user", "");
            String passwd = data.getOrDefault("passwd", "");
            if (user.length() == 0 || passwd.length() == 0)
                return "false";

            String ldapUser = "cn=" + user + "," + authPeopleDir;

            Hashtable env = new Hashtable(11);
            env.put(Context.INITIAL_CONTEXT_FACTORY,
                    "com.sun.jndi.ldap.LdapCtxFactory");
            env.put(Context.PROVIDER_URL, "ldap://" + authAddress);

            // Authenticate as S. User and give incorrect password
            env.put(Context.SECURITY_AUTHENTICATION, "simple");
            env.put(Context.SECURITY_PRINCIPAL, ldapUser);
            env.put(Context.SECURITY_CREDENTIALS, passwd);

            try {
                DirContext ctx = new InitialDirContext(env);
                LdapContext lctx = (LdapContext) ctx.lookup(ldapUser);

                SearchControls ctrls = new SearchControls();
                ctrls.setSearchScope(SearchControls.SUBTREE_SCOPE);
                ctrls.setReturningAttributes(new String[] {"memberOf"});
                final NamingEnumeration results = lctx.search("", "(objectClass=*)", ctrls);
                while (results.hasMore()) {
                    final SearchResult r = (SearchResult) results.nextElement();
                    final Attribute attr = r.getAttributes().get("memberOf");
                    if (attr != null)
                        for (Enumeration en = attr.getAll(); en.hasMoreElements(); ) {
                            if (en.nextElement().toString().equalsIgnoreCase(authGroup)) {
                                ctx.close();
                                return "true";
                            }
                        }
                }
                ctx.close();
            } catch (NamingException e) {
            }
            return "false";
        }
        public void configure() {
            DataFormat format = new JacksonDataFormat();

            //restConfiguration().component("servlet").bindingMode(RestBindingMode.json);
            rest("/places").produces("application/json")
                    .get("/{name}/location")
                    .to("direct:getLocation")
                    .get("/{name}/neighbors")
                    .to("direct:getNeighbors")
                    .get("/{location}/county")
                    .to("direct:getCounty")
                    .get("/{name}/info")
                    .to("direct:getInfo");
            rest("/auth").produces("application/json")
                    .post().route()
                    .unmarshal(format)
                    .bean(method(this, "doAuth"))
                    .transform().body();
            from("direct:getLocation")
                    .removeHeaders("CamelHttp*")
                    .toD("rest:get:location/${header.name}?bridgeEndpoint=true&host={{servers.location}}")
                    .convertBodyTo(String.class).transform().body();
            from("direct:getNeighbors")
                    .removeHeaders("CamelHttp*")
                    .toD("rest:get:neighbors/${header.name}?bridgeEndpoint=true&host={{servers.location}}")
                    .convertBodyTo(String.class).transform().body();
            from("direct:getCounty")
                    .removeHeaders("CamelHttp*")
                    .toD("rest:get:county/${header.location}?bridgeEndpoint=true&host={{servers.location}}")
                    .convertBodyTo(String.class).transform().body();
            from("direct:getInfo")
                    .removeHeaders("CamelHttp*")
                    .toD("rest:get:page/${header.name}?bridgeEndpoint=true&host={{servers.wiki}}")
                    .convertBodyTo(String.class).transform().body();
        }
    }

}
