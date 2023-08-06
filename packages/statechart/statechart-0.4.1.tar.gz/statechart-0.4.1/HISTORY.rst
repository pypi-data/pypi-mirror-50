=======
History
=======

0.2.0 (2016-08-02)
------------------

* First release on PyPI.

0.2.1 (2016-08-07)
------------------

* Final state bug fixes.

0.2.2 (2016-08-08)
------------------

* Default transition bug fix.

0.2.3 (2016-08-10)
------------------

* Consume event dispatched by child state unless a final state activated.

0.2.4 (2016-08-21)
------------------

* Fix internal transition acting like local transition.

0.3.0 (2016-10-16)
------------------

* Implement display module to generate Plant UML code of a statechart.
* Raise runtime exception if an action is defined on top level statechart.

0.3.1 (2016-10-16)
------------------

* Implement specific statechart deactivate function.

0.4.0 (2019-05-18)
------------------

* Add support for functional action and guard definitions.
* Deprecate KwEvent, Internal Transitions, Actions and Guard
* Add support for generating PlantUML diagrams.

0.4.0 (2019-08-15)
------------------

* Fix display of guard function names in PlantUML diagrams.
* Allow any type of value to be used for event data.
