select id, name, loc <-> location::geometry as dist from miejsca m, (select location::geometry as loc from miejsca where id = 80112) war order by loc <-> location::geometry limit 30;
