/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.jena.mem;

import java.util.*;
import java.util.function.Consumer;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

import org.apache.jena.graph.* ;
import org.apache.jena.graph.Triple.Field ;
import org.apache.jena.util.iterator.* ;

/**
    A base class for in-memory graphs
*/
public abstract class NodeToTriplesMapBase
    {
    /**
         The map from nodes to Bunch(Triple).
    */
     public BunchMap bunchMap = new HashedBunchMap();

    /**
         The number of triples held in this NTM, maintained incrementally 
         (because it's a pain to compute from scratch).
    */
    protected int size = 0;

    protected final Field indexField;
    protected final Field f2;
    protected final Field f3;
    
    public NodeToTriplesMapBase( Field indexField, Field f2, Field f3 )
        { this.indexField = indexField; this.f2 = f2; this.f3 = f3; }
    
    /**
         Add <code>t</code> to this NTM; the node <code>o</code> <i>must</i>
         be the index node of the triple. Answer <code>true</code> iff the triple
         was not previously in the set, ie, it really truly has been added. 
    */
    public abstract boolean add( Triple t );

    /**
         Remove <code>t</code> from this NTM. Answer <code>true</code> iff the 
         triple was previously in the set, ie, it really truly has been removed. 
    */
    public abstract boolean remove( Triple t );

    public abstract ExtendedIterator<Triple> iterator( Object o, HashCommon.NotifyEmpty container );

    /**
         Answer true iff this NTM contains the concrete triple <code>t</code>.
    */
    public abstract boolean contains( Triple t );
    
    public abstract boolean containsBySameValueAs( Triple t );

    /**
        The values (usually nodes) which appear in the index position of the stored triples; useful
        for eg listSubjects().
    */
    public final Iterator<Object> domain()
        { return bunchMap.keyIterator(); }

    protected final Object getIndexField( Triple t )
        { return indexField.getField( t ).getIndexingValue(); }

    /**
        Clear this NTM; it will contain no triples.
    */
    public void clear()
        { bunchMap.clear(); size = 0; }

    public int size()
        { return size; }

    public void removedOneViaIterator()
        { size -= 1; }

    public boolean isEmpty()
        { return size == 0; }

    public abstract ExtendedIterator<Triple> iterator( Node index, Node n2, Node n3 );
    
    /**
        Answer an iterator over all the triples that are indexed by the item <code>y</code>.
        Note that <code>y</code> need not be a Node (because of indexing values).
    */
    public abstract ExtendedIterator<Triple> iteratorForIndexed( Object y );
    
    /**
        Answer an iterator over all the triples in this NTM.
    */
    public ExtendedIterator<Triple> iterateAll()
        {
        return new NiceIterator<Triple>() 
            {
            private final Iterator<TripleBunch> bunchIterator = bunchMap.iterator();
            private Iterator<Triple> current = NullIterator.instance();
            private NotifyMe emptier = new NotifyMe();
            
            @Override public Triple next()
                {
                if (!hasNext()) noElements( "NodeToTriples iterator" );
                return current.next();
                }

            class NotifyMe implements HashCommon.NotifyEmpty
                {
                @Override
                public void emptied()
                    { bunchIterator.remove(); }
                }
            
            @Override public boolean hasNext()
                {
                while (true)
                    {
                    if (current.hasNext()) return true;
                    if (!bunchIterator.hasNext()) return false;
                    current = bunchIterator.next().iterator( emptier );
                    }
                }

            @Override public void forEachRemaining(Consumer<? super Triple> action)
                {
                if (current != null) current.forEachRemaining(action);
                bunchIterator.forEachRemaining(next ->
                    {
                    current = next.iterator();
                    current.forEachRemaining(action);
                    });
                }

                @Override public void remove()
                { current.remove(); }
            };
        }


        public Stream<Triple> streamAll()
            {
            return StreamSupport.stream(bunchMap.spliterator(), false)
                    .flatMap(bunch -> StreamSupport.stream(bunch.spliterator(), false));
            }

        public Stream<Triple> stream( Node index, Node n2, Node n3 )
            {
            Object indexValue = index.getIndexingValue();
            TripleBunch s = bunchMap.get( indexValue );
            if (s == null) return Stream.empty();
            var filter = FieldFilter.filterOn(f2, n2, f3, n3);
            return filter.hasFilter()
                    ? StreamSupport.stream(s.spliterator(), false).filter(filter.getFilter())
                    : StreamSupport.stream(s.spliterator(), false);
            }

        public boolean containsMatch( Node index, Node n2, Node n3 )
            {
            TripleBunch s = bunchMap.get( index.getIndexingValue() );
            if (s == null)
                return false;
            var filter = FieldFilter.filterOn(f2, n2, f3, n3);
            if (!filter.hasFilter())
                return true;
            var spliterator = s.spliterator();
            final boolean[] found = {false};
            Consumer<Triple> tester = triple -> found[0] = filter.getFilter().test(triple);
            while (!found[0] && spliterator.tryAdvance(tester));
            return found[0];
            }
    }
